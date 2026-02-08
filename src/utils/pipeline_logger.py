"""
Pipeline Logger for Smokemirror.

Captures and saves intermediate steps of the story generation pipeline
for debugging, analysis, and understanding the generation process.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)


@dataclass
class GenerationStep:
    """Represents a single step in the generation pipeline."""
    step_name: str
    step_type: str  # "prompt", "response", "decision", "evaluation"
    timestamp: str
    input_data: Optional[dict] = None
    output_data: Optional[dict] = None
    prompt: Optional[str] = None
    response: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


class PipelineLogger:
    """Logs and saves intermediate steps of the story generation pipeline."""

    def __init__(self, output_dir: Path, run_id: str):
        """Initialize the pipeline logger.

        Args:
            output_dir: Directory to save logs
            run_id: Unique identifier for this run
        """
        self.output_dir = Path(output_dir)
        self.run_id = run_id
        self.steps: list[GenerationStep] = []
        self.section_counts: dict[str, int] = {}

        # Create pipeline logs directory
        self.logs_dir = self.output_dir / "pipeline_logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"PipelineLogger initialized: {self.logs_dir}")

    def log_step(
        self,
        step_name: str,
        step_type: str,
        input_data: Optional[dict] = None,
        output_data: Optional[dict] = None,
        prompt: Optional[str] = None,
        response: Optional[str] = None,
        **metadata
    ) -> GenerationStep:
        """Log a generation step.

        Args:
            step_name: Name of the step (e.g., "crime_backstory", "plot_point_5")
            step_type: Type of step ("prompt", "response", "decision", "evaluation")
            input_data: Input data for this step
            output_data: Output data from this step
            prompt: The prompt sent to the LLM
            response: The response from the LLM
            **metadata: Additional metadata

        Returns:
            The logged GenerationStep
        """
        step = GenerationStep(
            step_name=step_name,
            step_type=step_type,
            timestamp=datetime.now().isoformat(),
            input_data=input_data,
            output_data=output_data,
            prompt=prompt,
            response=response,
            metadata=metadata,
        )
        self.steps.append(step)

        # Also save individual step file for large prompts/responses
        if prompt or response:
            self._save_step_file(step)

        return step

    def log_prompt_response(
        self,
        section: str,
        prompt: str,
        response: str,
        parsed_output: Optional[dict] = None,
        **metadata
    ):
        """Convenience method to log a prompt-response pair.

        Args:
            section: Section name (e.g., "backstory", "plot_point", "reader_eval")
            prompt: The prompt sent
            response: The response received
            parsed_output: Parsed/structured output if available
            **metadata: Additional metadata
        """
        # Track section counts for numbering
        if section not in self.section_counts:
            self.section_counts[section] = 0
        self.section_counts[section] += 1

        step_name = f"{section}_{self.section_counts[section]}"

        self.log_step(
            step_name=step_name,
            step_type="prompt_response",
            prompt=prompt,
            response=response,
            output_data=parsed_output,
            **metadata
        )

    def log_reader_evaluation(
        self,
        reader_role: str,
        story_text: str,
        prompt: str,
        response: str,
        evaluation: dict,
    ):
        """Log a reader evaluation step.

        Args:
            reader_role: Role of the reader (logic_analyst, etc.)
            story_text: The story text being evaluated
            prompt: The evaluation prompt
            response: Raw response from reader LLM
            evaluation: Parsed evaluation results
        """
        self.log_step(
            step_name=f"reader_eval_{reader_role}",
            step_type="evaluation",
            input_data={"story_length": len(story_text)},
            output_data=evaluation,
            prompt=prompt,
            response=response,
            reader_role=reader_role,
        )

    def _save_step_file(self, step: GenerationStep):
        """Save a step to its own file for detailed inspection.

        Args:
            step: The step to save
        """
        # Sanitize filename
        safe_name = step.step_name.replace("/", "_").replace(" ", "_")
        filename = f"{safe_name}_{step.step_type}.json"

        with open(self.logs_dir / filename, "w", encoding="utf-8") as f:
            json.dump(step.to_dict(), f, indent=2, ensure_ascii=False)

    def save_summary(self):
        """Save a summary of all pipeline steps."""
        summary = {
            "run_id": self.run_id,
            "total_steps": len(self.steps),
            "section_counts": self.section_counts,
            "steps": [
                {
                    "step_name": s.step_name,
                    "step_type": s.step_type,
                    "timestamp": s.timestamp,
                    "has_prompt": s.prompt is not None,
                    "has_response": s.response is not None,
                    "prompt_length": len(s.prompt) if s.prompt else 0,
                    "response_length": len(s.response) if s.response else 0,
                    "metadata": s.metadata,
                }
                for s in self.steps
            ],
        }

        with open(self.logs_dir / "pipeline_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        logger.info(f"Pipeline summary saved: {len(self.steps)} steps logged")

    def save_full_log(self):
        """Save the complete log with all prompts and responses."""
        full_log = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "total_steps": len(self.steps),
            "steps": [s.to_dict() for s in self.steps],
        }

        with open(self.logs_dir / "full_pipeline_log.json", "w", encoding="utf-8") as f:
            json.dump(full_log, f, indent=2, ensure_ascii=False)

        logger.info(f"Full pipeline log saved to {self.logs_dir / 'full_pipeline_log.json'}")

    def save_reader_evaluations(self, evaluations: list[dict]):
        """Save detailed reader evaluations to a separate file.

        Args:
            evaluations: List of reader evaluation dictionaries
        """
        eval_data = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "num_evaluations": len(evaluations),
            "evaluations": evaluations,
        }

        with open(self.output_dir / "reader_evaluations.json", "w", encoding="utf-8") as f:
            json.dump(eval_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Reader evaluations saved: {len(evaluations)} evaluations")

    def get_step_by_name(self, step_name: str) -> Optional[GenerationStep]:
        """Get a specific step by name.

        Args:
            step_name: Name of the step to find

        Returns:
            The step if found, None otherwise
        """
        for step in self.steps:
            if step.step_name == step_name:
                return step
        return None

    def get_steps_by_type(self, step_type: str) -> list[GenerationStep]:
        """Get all steps of a specific type.

        Args:
            step_type: Type of steps to find

        Returns:
            List of matching steps
        """
        return [s for s in self.steps if s.step_type == step_type]
