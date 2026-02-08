"""
LLM Wrapper for Qwen3 and other models.
Provides a unified interface for text generation.
"""

import json
import re
import logging
from dataclasses import dataclass
from typing import Optional, Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from ..utils.config import ModelConfig

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Response from LLM generation."""
    text: str
    parsed_json: Optional[dict] = None
    tokens_generated: int = 0
    success: bool = True
    error: Optional[str] = None


class LLMWrapper:
    """Wrapper for local LLM models using Hugging Face transformers."""

    def __init__(self, config: ModelConfig):
        """Initialize the LLM wrapper.

        Args:
            config: Model configuration
        """
        self.config = config
        self.model = None
        self.tokenizer = None
        self._load_model()

    def _load_model(self):
        """Load the model and tokenizer."""
        logger.info(f"Loading model: {self.config.name}")

        # Configure quantization if requested
        quantization_config = None
        if self.config.load_in_4bit:
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=getattr(torch, self.config.torch_dtype),
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )
        elif self.config.load_in_8bit:
            quantization_config = BitsAndBytesConfig(load_in_8bit=True)

        # Determine device
        if self.config.device == "auto":
            device_map = "auto"
        else:
            device_map = self.config.device

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.name,
            trust_remote_code=True,
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.name,
            quantization_config=quantization_config,
            device_map=device_map,
            torch_dtype=getattr(torch, self.config.torch_dtype),
            trust_remote_code=True,
        )
        self.model.eval()

        logger.info(f"Model loaded successfully on device: {device_map}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_new_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        expect_json: bool = False,
        disable_thinking: bool = False,
    ) -> LLMResponse:
        """Generate text from the model.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            max_new_tokens: Override max tokens
            temperature: Override temperature
            expect_json: Whether to parse response as JSON
            disable_thinking: Whether to disable Qwen3 thinking mode (saves tokens)

        Returns:
            LLMResponse with generated text and optional parsed JSON
        """
        # Build messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # For Qwen3 models: add /no_think to disable thinking mode (saves tokens)
        # Qwen2.5 and other models don't support this tag
        is_qwen3 = "qwen3" in self.config.name.lower()
        if is_qwen3 and (expect_json or disable_thinking):
            prompt = prompt + "\n\n/no_think"

        messages.append({"role": "user", "content": prompt})

        # Apply chat template
        try:
            input_text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        except Exception:
            # Fallback for models without chat template
            if system_prompt:
                input_text = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
            else:
                input_text = f"User: {prompt}\n\nAssistant:"

        # Tokenize
        inputs = self.tokenizer(input_text, return_tensors="pt")
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens or self.config.max_new_tokens,
                temperature=temperature or self.config.temperature,
                top_p=self.config.top_p,
                top_k=self.config.top_k,
                do_sample=self.config.do_sample,
                repetition_penalty=self.config.repetition_penalty,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )

        # Decode only new tokens
        input_length = inputs["input_ids"].shape[1]
        generated_tokens = outputs[0][input_length:]
        generated_text = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
        tokens_generated = len(generated_tokens)

        # Parse JSON if expected
        parsed_json = None
        if expect_json:
            parsed_json = self._extract_json(generated_text)

        return LLMResponse(
            text=generated_text.strip(),
            parsed_json=parsed_json,
            tokens_generated=tokens_generated,
            success=True,
        )

    def _strip_thinking_tags(self, text: str) -> str:
        """Remove Qwen3 thinking tags from response.

        Args:
            text: Text that may contain <think>...</think> tags

        Returns:
            Text with thinking tags removed
        """
        # Remove <think>...</think> blocks (Qwen3 reasoning)
        text = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.MULTILINE)
        # Also handle unclosed think tags
        text = re.sub(r"<think>[\s\S]*$", "", text, flags=re.MULTILINE)
        return text.strip()

    def _extract_json(self, text: str) -> Optional[dict]:
        """Extract JSON from generated text.

        Args:
            text: Text that may contain JSON

        Returns:
            Parsed JSON dict or None
        """
        # First, strip thinking tags (Qwen3 specific)
        text = self._strip_thinking_tags(text)

        # Try to find JSON block
        json_patterns = [
            r"```json\s*([\s\S]*?)\s*```",  # Markdown code block
            r"```\s*([\s\S]*?)\s*```",  # Generic code block
            r"\{[\s\S]*\}",  # Raw JSON object
        ]

        for pattern in json_patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            for match in matches:
                try:
                    # Clean the match
                    json_str = match.strip()
                    if not json_str.startswith("{"):
                        # Find the JSON object within the match
                        start = json_str.find("{")
                        end = json_str.rfind("}") + 1
                        if start != -1 and end > start:
                            json_str = json_str[start:end]

                    return json.loads(json_str)
                except json.JSONDecodeError:
                    continue

        # Try parsing the entire text as JSON
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON from response")
            return None

    def generate_with_retry(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_retries: int = 3,
        expect_json: bool = False,
        **kwargs,
    ) -> LLMResponse:
        """Generate with retry logic for JSON parsing failures.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            max_retries: Maximum retry attempts
            expect_json: Whether to parse response as JSON
            **kwargs: Additional generation parameters

        Returns:
            LLMResponse with generated text
        """
        for attempt in range(max_retries):
            response = self.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                expect_json=expect_json,
                **kwargs,
            )

            if not expect_json or response.parsed_json is not None:
                return response

            logger.warning(f"JSON parsing failed, attempt {attempt + 1}/{max_retries}")

            # Add explicit instruction for retry
            if attempt < max_retries - 1:
                prompt = prompt + "\n\nIMPORTANT: Respond ONLY with valid JSON. No other text."

        # Return last response even if JSON parsing failed
        response.success = False
        response.error = "Failed to generate valid JSON after retries"
        return response

    def batch_generate(
        self,
        prompts: list[str],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> list[LLMResponse]:
        """Generate responses for multiple prompts.

        Args:
            prompts: List of prompts
            system_prompt: Optional system prompt (shared)
            **kwargs: Additional generation parameters

        Returns:
            List of LLMResponse objects
        """
        # For simplicity, process sequentially
        # Could be optimized with batching for throughput
        responses = []
        for prompt in prompts:
            response = self.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                **kwargs,
            )
            responses.append(response)
        return responses


class MockLLMWrapper:
    """Mock LLM wrapper for testing without GPU."""

    def __init__(self, config: ModelConfig):
        self.config = config
        logger.info("Using MockLLMWrapper for testing")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        expect_json: bool = False,
        **kwargs,
    ) -> LLMResponse:
        """Generate mock response."""
        if expect_json:
            # Return a mock JSON response based on prompt content
            mock_json = self._generate_mock_json(prompt)
            return LLMResponse(
                text=json.dumps(mock_json, indent=2),
                parsed_json=mock_json,
                tokens_generated=100,
                success=True,
            )

        return LLMResponse(
            text="This is a mock response for testing purposes.",
            tokens_generated=10,
            success=True,
        )

    def _generate_mock_json(self, prompt: str) -> dict:
        """Generate appropriate mock JSON based on prompt type."""
        if "crime backstory" in prompt.lower():
            return {
                "crime_type": "murder",
                "victim": {"name": "James Wilson", "occupation": "auditor"},
                "criminal": {"name": "David Chen", "occupation": "CFO", "motive": "embezzlement cover-up"},
                "conspirators": [{"name": "Alice", "role": "lure victim"}],
                "method": "staged accident",
                "timeline": [{"time": "9:00 PM", "event": "crime occurred"}],
                "evidence": [{"id": "E1", "description": "security footage gap"}],
                "location": "parking garage",
                "coordination_plan": "synchronized alibis",
            }
        elif "fabricated" in prompt.lower():
            return {
                "fake_suspect": {"name": "Eric Thompson", "fake_motive": "revenge"},
                "fake_timeline": [{"time": "8:45 PM", "event": "suspect entered building"}],
                "planted_evidence": [{"id": "PE1", "description": "fingerprints"}],
                "alibis": {"Alice": "at home", "Bob": "at gym"},
                "cover_story": "disgruntled former employee",
            }
        elif "collision" in prompt.lower():
            return {
                "is_collision": True,
                "collision_severity": "moderate",
                "threatened_conspirators": ["Bob"],
                "vulnerable_point": "security footage",
                "intervention_urgency": "medium",
            }
        else:
            return {"status": "mock_response", "data": {}}

    def generate_with_retry(self, *args, **kwargs) -> LLMResponse:
        return self.generate(*args, **kwargs)

    def batch_generate(self, prompts: list[str], **kwargs) -> list[LLMResponse]:
        return [self.generate(p, **kwargs) for p in prompts]


def create_llm_wrapper(config: ModelConfig, use_mock: bool = False) -> LLMWrapper:
    """Factory function to create LLM wrapper.

    Args:
        config: Model configuration
        use_mock: Whether to use mock wrapper for testing

    Returns:
        LLMWrapper or MockLLMWrapper instance
    """
    if use_mock:
        return MockLLMWrapper(config)

    try:
        return LLMWrapper(config)
    except Exception as e:
        logger.warning(f"Failed to load real model: {e}. Falling back to mock.")
        return MockLLMWrapper(config)
