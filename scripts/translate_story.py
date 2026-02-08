#!/usr/bin/env python3
"""
Translate a story from English to Chinese using Qwen model.
"""

import os
import sys
import re
import logging
from pathlib import Path

# Set HuggingFace cache before imports
os.environ["HF_HOME"] = "/coc/pskynet6/jhe478/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/coc/pskynet6/jhe478/huggingface"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Translate story to Chinese")
    parser.add_argument("--input", type=str, required=True, help="Input story file")
    parser.add_argument("--output", type=str, default=None, help="Output file (default: input_chinese.md)")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-7B-Instruct", help="Model to use")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        return 1

    output_path = Path(args.output) if args.output else input_path.with_name(input_path.stem + "_chinese.md")

    logger.info("=" * 60)
    logger.info("STORY TRANSLATION - English to Chinese")
    logger.info("=" * 60)
    logger.info(f"Input: {input_path}")
    logger.info(f"Output: {output_path}")
    logger.info(f"Model: {args.model}")

    # Load model
    logger.info("\nLoading model...")
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    logger.info("Model loaded successfully")

    # Read input story
    with open(input_path, "r", encoding="utf-8") as f:
        story = f.read()

    logger.info(f"Story length: {len(story)} characters")

    # Split story into chunks (by chapters/sections)
    sections = re.split(r'(^## .+$)', story, flags=re.MULTILINE)

    # Reconstruct sections with their headers
    chunks = []
    current_chunk = ""
    for i, section in enumerate(sections):
        if section.startswith("## "):
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = section
        else:
            current_chunk += section
    if current_chunk:
        chunks.append(current_chunk)

    logger.info(f"Split into {len(chunks)} chunks for translation")

    # Translate each chunk
    translated_chunks = []
    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            translated_chunks.append(chunk)
            continue

        logger.info(f"Translating chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")

        prompt = f"""Please translate the following English text to Chinese.
Maintain the original formatting including markdown headers, italics, and paragraph structure.
Keep character names in their original English form but you can add Chinese transliteration in parentheses on first appearance.
Translate naturally and fluently, preserving the literary style and atmosphere.

Text to translate:
{chunk}

Chinese translation:"""

        messages = [{"role": "user", "content": prompt}]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        inputs = tokenizer(text, return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=4096,
                temperature=0.3,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )

        response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)

        # Clean up response
        if "<think>" in response:
            response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)

        translated_chunks.append(response.strip())
        logger.info(f"  Translated to {len(response)} chars")

    # Combine translated chunks
    translated_story = "\n\n".join(translated_chunks)

    # Save output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(translated_story)

    logger.info("\n" + "=" * 60)
    logger.info("TRANSLATION COMPLETED!")
    logger.info("=" * 60)
    logger.info(f"Output saved to: {output_path}")
    logger.info(f"Original length: {len(story)} chars")
    logger.info(f"Translated length: {len(translated_story)} chars")

    return 0


if __name__ == "__main__":
    sys.exit(main())
