"""
Reader Simulation Module

Simulates different types of readers evaluating the generated story
for suspense quality, logical consistency, and narrative coherence.
"""

import json
import logging
from dataclasses import dataclass
from typing import Optional
from enum import Enum

from ..models.llm_wrapper import LLMWrapper
from ..data_structures.facts import (
    PlotPoint,
    ReaderEvaluation,
    IssueSeverity,
    CrimeFacts,
)
from ..utils.prompts import PromptTemplates
from ..utils.config import ReaderSimulationConfig

logger = logging.getLogger(__name__)


class ReaderRole(Enum):
    """Types of simulated readers."""
    LOGIC_ANALYST = "logic_analyst"
    INTUITIVE_READER = "intuitive_reader"
    GENRE_EXPERT = "genre_expert"


@dataclass
class ReaderProfile:
    """Profile for a simulated reader."""
    role: ReaderRole
    focus: str
    weight: float = 1.0


class ReaderSimulator:
    """Simulates readers evaluating the story."""

    def __init__(
        self,
        llm: LLMWrapper,
        config: ReaderSimulationConfig,
    ):
        """Initialize the simulator.

        Args:
            llm: LLM wrapper for simulation
            config: Reader simulation configuration
        """
        self.llm = llm
        self.config = config
        self.reader_profiles = self._setup_reader_profiles()

    def _setup_reader_profiles(self) -> list[ReaderProfile]:
        """Set up reader profiles from config.

        Returns:
            List of ReaderProfile objects
        """
        profiles = []
        for role_config in self.config.reader_roles:
            try:
                role = ReaderRole(role_config.name)
            except ValueError:
                role = ReaderRole.LOGIC_ANALYST

            profiles.append(ReaderProfile(
                role=role,
                focus=role_config.focus,
                weight=role_config.weight,
            ))

        # Ensure we have at least one reader
        if not profiles:
            profiles = [
                ReaderProfile(
                    role=ReaderRole.LOGIC_ANALYST,
                    focus="logical consistency and deduction",
                    weight=1.5,
                ),
                ReaderProfile(
                    role=ReaderRole.INTUITIVE_READER,
                    focus="character behavior and immersion",
                    weight=1.0,
                ),
                ReaderProfile(
                    role=ReaderRole.GENRE_EXPERT,
                    focus="pacing and narrative structure",
                    weight=1.2,
                ),
            ]

        return profiles

    def evaluate_story(
        self,
        plot_points: list[PlotPoint],
        real_facts: Optional[CrimeFacts] = None,
    ) -> list[ReaderEvaluation]:
        """Evaluate story using all simulated readers.

        Args:
            plot_points: Story plot points
            real_facts: Real crime facts (for checking if readers solve the mystery)

        Returns:
            List of ReaderEvaluation objects
        """
        if not self.config.enabled:
            logger.info("Reader simulation disabled")
            return []

        evaluations = []

        # Format story for readers (detective perspective only)
        story_text = self._format_story_for_readers(plot_points)

        for profile in self.reader_profiles:
            logger.info(f"Running {profile.role.value} evaluation")

            evaluation = self._run_reader_evaluation(
                profile=profile,
                story_text=story_text,
                plot_points=plot_points,
                real_facts=real_facts,
            )
            evaluations.append(evaluation)

        return evaluations

    def _format_story_for_readers(self, plot_points: list[PlotPoint]) -> str:
        """Format plot points as a story for reader evaluation.

        The readers only see the detective's perspective, not the reader revelations.

        Args:
            plot_points: Story plot points

        Returns:
            Formatted story text
        """
        story_parts = []
        for pp in plot_points:
            part = f"[Plot Point {pp.id}]\n"
            if pp.detective_action:
                part += f"The detective {pp.detective_action}. "
            part += pp.description
            if pp.detective_learns:
                part += f" The detective learns: {pp.detective_learns}."
            if pp.obstacle:
                part += f" Obstacle encountered: {pp.obstacle}."
            story_parts.append(part)

        return "\n\n".join(story_parts)

    def _run_reader_evaluation(
        self,
        profile: ReaderProfile,
        story_text: str,
        plot_points: list[PlotPoint],
        real_facts: Optional[CrimeFacts],
    ) -> ReaderEvaluation:
        """Run evaluation for a single reader type.

        Args:
            profile: Reader profile
            story_text: Formatted story
            plot_points: Original plot points
            real_facts: Real crime facts

        Returns:
            ReaderEvaluation object
        """
        # Get appropriate prompt for this reader role
        prompt_template = PromptTemplates.get_reader_prompt(profile.role.value)

        prompt = prompt_template.format(
            story=story_text,
            checkpoints=", ".join(str(c) for c in self.config.checkpoints),
        )

        response = self.llm.generate_with_retry(
            prompt=prompt,
            expect_json=True,
            max_new_tokens=2048,
        )

        # Parse response
        return self._parse_reader_response(
            response.parsed_json or {},
            profile,
            plot_points,
            real_facts,
        )

    def _parse_reader_response(
        self,
        data: dict,
        profile: ReaderProfile,
        plot_points: list[PlotPoint],
        real_facts: Optional[CrimeFacts],
    ) -> ReaderEvaluation:
        """Parse LLM response into ReaderEvaluation.

        Args:
            data: Parsed JSON response
            profile: Reader profile
            plot_points: Plot points for validation
            real_facts: Real crime facts

        Returns:
            ReaderEvaluation object
        """
        # Parse suspense scores
        suspense_scores = {}
        raw_scores = data.get("suspense_scores", {})
        for pp_id, score in raw_scores.items():
            try:
                suspense_scores[int(pp_id)] = float(score)
            except (ValueError, TypeError):
                continue

        # Fill in missing scores with defaults
        for pp in plot_points:
            if pp.id not in suspense_scores:
                suspense_scores[pp.id] = 5.0  # Neutral default

        # Parse criminal predictions
        criminal_predictions = {}
        raw_predictions = data.get("criminal_predictions", {})
        for checkpoint, pred in raw_predictions.items():
            if isinstance(pred, dict):
                criminal_predictions[int(checkpoint) if str(checkpoint).isdigit() else checkpoint] = pred

        # Check if reader correctly identified real criminal
        if real_facts:
            for checkpoint, pred in criminal_predictions.items():
                if isinstance(pred, dict) and pred.get("prediction", "").lower() == real_facts.criminal.name.lower():
                    # Reader figured it out - this is a problem!
                    logger.warning(
                        f"{profile.role.value} correctly identified criminal at checkpoint {checkpoint}"
                    )

        # Parse inconsistency flags
        inconsistency_flags = []
        for flag in data.get("inconsistency_flags", []):
            if isinstance(flag, dict):
                severity_str = flag.get("severity", "minor")
                try:
                    severity = IssueSeverity(severity_str)
                except ValueError:
                    severity = IssueSeverity.MINOR

                inconsistency_flags.append({
                    "plot_point": flag.get("plot_point", 0),
                    "issue": flag.get("issue", "Unknown issue"),
                    "severity": severity,
                })

        # Parse engagement assessment
        engagement = data.get("engagement_assessment", {
            "most_engaging": [],
            "least_engaging": [],
            "comments": "No assessment provided",
        })

        # Calculate overall score
        if suspense_scores:
            avg_suspense = sum(suspense_scores.values()) / len(suspense_scores)
        else:
            avg_suspense = 5.0

        # Penalize for issues
        issue_penalty = sum(
            1.0 if f["severity"] == IssueSeverity.CRITICAL else
            0.5 if f["severity"] == IssueSeverity.MODERATE else 0.2
            for f in inconsistency_flags
        )

        overall_score = max(1.0, min(10.0, avg_suspense - issue_penalty))

        return ReaderEvaluation(
            reader_role=profile.role.value,
            suspense_scores=suspense_scores,
            criminal_predictions=criminal_predictions,
            inconsistency_flags=inconsistency_flags,
            engagement_assessment=engagement,
            overall_score=overall_score * profile.weight,
        )

    def get_suspense_curve(
        self,
        evaluations: list[ReaderEvaluation],
    ) -> dict[int, float]:
        """Aggregate suspense scores into a curve.

        Args:
            evaluations: Reader evaluations

        Returns:
            Dict mapping plot point ID to average suspense score
        """
        if not evaluations:
            return {}

        # Collect all scores per plot point
        all_scores: dict[int, list[float]] = {}
        for eval in evaluations:
            for pp_id, score in eval.suspense_scores.items():
                if pp_id not in all_scores:
                    all_scores[pp_id] = []
                all_scores[pp_id].append(score)

        # Average scores
        return {
            pp_id: sum(scores) / len(scores)
            for pp_id, scores in all_scores.items()
        }

    def analyze_suspense_curve(
        self,
        suspense_curve: dict[int, float],
    ) -> dict:
        """Analyze the suspense curve for issues.

        Args:
            suspense_curve: Suspense scores by plot point

        Returns:
            Analysis dict with identified issues
        """
        if not suspense_curve:
            return {"issues": [], "trend": "unknown"}

        scores = [suspense_curve[k] for k in sorted(suspense_curve.keys())]
        issues = []

        # Check for flat middle
        if len(scores) >= 6:
            middle_start = len(scores) // 3
            middle_end = 2 * len(scores) // 3
            middle_scores = scores[middle_start:middle_end]

            if max(middle_scores) - min(middle_scores) < 1.0:
                issues.append({
                    "type": "flat_middle",
                    "range": (middle_start, middle_end),
                    "description": "Suspense plateaus in the middle section",
                })

        # Check for premature peak
        if len(scores) >= 5:
            peak_idx = scores.index(max(scores))
            if peak_idx < len(scores) * 0.6:  # Peak before 60% of story
                issues.append({
                    "type": "premature_peak",
                    "position": peak_idx,
                    "description": "Suspense peaks too early",
                })

        # Check for sudden drops
        for i in range(1, len(scores)):
            if scores[i] < scores[i-1] - 2.0:  # Drop of more than 2 points
                issues.append({
                    "type": "sudden_drop",
                    "position": i,
                    "description": f"Sharp suspense drop at plot point {i}",
                })

        # Calculate overall trend
        if len(scores) >= 2:
            first_half_avg = sum(scores[:len(scores)//2]) / (len(scores)//2)
            second_half_avg = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)

            if second_half_avg > first_half_avg + 0.5:
                trend = "ascending"
            elif second_half_avg < first_half_avg - 0.5:
                trend = "descending"
            else:
                trend = "flat"
        else:
            trend = "unknown"

        return {
            "issues": issues,
            "trend": trend,
            "peak_position": scores.index(max(scores)) if scores else 0,
            "average": sum(scores) / len(scores) if scores else 0,
        }

    def check_layer_leak(
        self,
        evaluations: list[ReaderEvaluation],
        real_facts: CrimeFacts,
    ) -> bool:
        """Check if any reader correctly identified the real criminal.

        Args:
            evaluations: Reader evaluations
            real_facts: Real crime facts

        Returns:
            True if a layer leak was detected
        """
        real_criminal = real_facts.criminal.name.lower()

        for eval in evaluations:
            for checkpoint, pred in eval.criminal_predictions.items():
                if isinstance(pred, dict):
                    prediction = pred.get("prediction", "").lower()
                    confidence = pred.get("confidence", "low")

                    if prediction == real_criminal and confidence in ["medium", "high"]:
                        return True

        return False
