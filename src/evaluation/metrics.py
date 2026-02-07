"""
Evaluation Metrics

Metrics for evaluating generated mystery stories.
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

from ..data_structures.facts import (
    PlotPoint,
    ReaderEvaluation,
    CrimeFacts,
    FabricatedFacts,
    StoryState,
)

logger = logging.getLogger(__name__)


@dataclass
class StoryMetrics:
    """Comprehensive metrics for a generated story."""
    # Basic metrics
    num_plot_points: int = 0
    num_conspirator_interventions: int = 0
    num_obstacles: int = 0

    # Suspense metrics
    avg_suspense: float = 0.0
    suspense_variance: float = 0.0
    suspense_trend: str = "unknown"  # ascending, descending, flat
    peak_suspense: float = 0.0
    peak_position: float = 0.0  # Normalized position (0-1)

    # Discovery path metrics
    initial_paths: int = 0
    final_paths: int = 0
    paths_closed: int = 0
    path_close_rate: float = 0.0  # paths closed per plot point

    # Reader evaluation metrics
    avg_reader_score: float = 0.0
    logic_score: float = 0.0
    engagement_score: float = 0.0
    genre_score: float = 0.0

    # Dual-layer metrics
    layer_leak_detected: bool = False
    criminal_prediction_accuracy: float = 0.0  # Lower is better for mystery

    # Structural metrics
    collision_rate: float = 0.0  # Percentage of plot points with collisions
    intervention_effectiveness: float = 0.0

    # Quality flags
    has_flat_middle: bool = False
    has_premature_peak: bool = False
    has_sudden_drops: bool = False
    num_critical_issues: int = 0
    num_moderate_issues: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "basic": {
                "num_plot_points": self.num_plot_points,
                "num_conspirator_interventions": self.num_conspirator_interventions,
                "num_obstacles": self.num_obstacles,
            },
            "suspense": {
                "avg_suspense": round(self.avg_suspense, 2),
                "suspense_variance": round(self.suspense_variance, 2),
                "suspense_trend": self.suspense_trend,
                "peak_suspense": round(self.peak_suspense, 2),
                "peak_position": round(self.peak_position, 2),
            },
            "discovery_paths": {
                "initial_paths": self.initial_paths,
                "final_paths": self.final_paths,
                "paths_closed": self.paths_closed,
                "path_close_rate": round(self.path_close_rate, 3),
            },
            "reader_scores": {
                "avg_reader_score": round(self.avg_reader_score, 2),
                "logic_score": round(self.logic_score, 2),
                "engagement_score": round(self.engagement_score, 2),
                "genre_score": round(self.genre_score, 2),
            },
            "dual_layer": {
                "layer_leak_detected": self.layer_leak_detected,
                "criminal_prediction_accuracy": round(self.criminal_prediction_accuracy, 2),
            },
            "structural": {
                "collision_rate": round(self.collision_rate, 2),
                "intervention_effectiveness": round(self.intervention_effectiveness, 2),
            },
            "quality_flags": {
                "has_flat_middle": self.has_flat_middle,
                "has_premature_peak": self.has_premature_peak,
                "has_sudden_drops": self.has_sudden_drops,
                "num_critical_issues": self.num_critical_issues,
                "num_moderate_issues": self.num_moderate_issues,
            },
        }

    def get_overall_score(self) -> float:
        """Calculate overall quality score (0-100)."""
        score = 0.0

        # Suspense contribution (30 points)
        suspense_score = min(30, self.avg_suspense * 3)
        if self.suspense_trend == "ascending":
            suspense_score += 5
        score += suspense_score

        # Reader score contribution (25 points)
        score += min(25, self.avg_reader_score * 2.5)

        # Structural quality (20 points)
        structural_score = 20
        if self.has_flat_middle:
            structural_score -= 5
        if self.has_premature_peak:
            structural_score -= 5
        if self.has_sudden_drops:
            structural_score -= 3
        score += max(0, structural_score)

        # Dual-layer integrity (15 points)
        layer_score = 15
        if self.layer_leak_detected:
            layer_score = 0
        elif self.criminal_prediction_accuracy > 0.3:
            layer_score -= 5
        score += layer_score

        # Plot point count (10 points)
        if self.num_plot_points >= 15:
            score += 10
        elif self.num_plot_points >= 10:
            score += 7
        else:
            score += max(0, self.num_plot_points)

        # Penalty for critical issues
        score -= self.num_critical_issues * 5

        return max(0, min(100, score))


class MetricsCalculator:
    """Calculates metrics for story evaluation."""

    def calculate(
        self,
        plot_points: list[PlotPoint],
        state: StoryState,
        evaluations: list[ReaderEvaluation],
        real_facts: Optional[CrimeFacts] = None,
        initial_paths: int = 5,
    ) -> StoryMetrics:
        """Calculate comprehensive metrics for a story.

        Args:
            plot_points: Generated plot points
            state: Final story state
            evaluations: Reader evaluations
            real_facts: Real crime facts
            initial_paths: Number of initial discovery paths

        Returns:
            StoryMetrics object
        """
        metrics = StoryMetrics()

        # Basic metrics
        metrics.num_plot_points = len(plot_points)
        metrics.num_conspirator_interventions = sum(
            1 for pp in plot_points if pp.conspirator_intervention
        )
        metrics.num_obstacles = sum(
            1 for pp in plot_points if pp.obstacle
        )

        # Suspense metrics
        self._calculate_suspense_metrics(metrics, plot_points, evaluations)

        # Discovery path metrics
        metrics.initial_paths = initial_paths
        metrics.final_paths = len(state.get_open_paths())
        metrics.paths_closed = sum(
            len(pp.paths_closed) for pp in plot_points
        )
        if metrics.num_plot_points > 0:
            metrics.path_close_rate = metrics.paths_closed / metrics.num_plot_points

        # Reader evaluation metrics
        self._calculate_reader_metrics(metrics, evaluations, real_facts)

        # Structural metrics
        if metrics.num_plot_points > 0:
            metrics.collision_rate = sum(
                1 for pp in plot_points if pp.is_collision
            ) / metrics.num_plot_points

        return metrics

    def _calculate_suspense_metrics(
        self,
        metrics: StoryMetrics,
        plot_points: list[PlotPoint],
        evaluations: list[ReaderEvaluation],
    ):
        """Calculate suspense-related metrics.

        Args:
            metrics: Metrics object to update
            plot_points: Plot points
            evaluations: Reader evaluations
        """
        # Get suspense scores from plot points
        pp_suspense = [pp.suspense_level for pp in plot_points]

        if not pp_suspense:
            return

        # Also incorporate reader evaluations if available
        reader_suspense = []
        for eval in evaluations:
            if eval.suspense_scores:
                reader_suspense.extend(eval.suspense_scores.values())

        # Combine (prefer reader scores if available)
        all_scores = reader_suspense if reader_suspense else pp_suspense

        # Calculate statistics
        metrics.avg_suspense = sum(all_scores) / len(all_scores)
        mean = metrics.avg_suspense
        metrics.suspense_variance = sum((s - mean) ** 2 for s in all_scores) / len(all_scores)

        # Peak analysis
        metrics.peak_suspense = max(all_scores)
        peak_idx = all_scores.index(metrics.peak_suspense)
        metrics.peak_position = peak_idx / len(all_scores) if all_scores else 0

        # Trend analysis
        if len(all_scores) >= 4:
            first_half = sum(all_scores[:len(all_scores)//2]) / (len(all_scores)//2)
            second_half = sum(all_scores[len(all_scores)//2:]) / (len(all_scores) - len(all_scores)//2)

            if second_half > first_half + 0.5:
                metrics.suspense_trend = "ascending"
            elif second_half < first_half - 0.5:
                metrics.suspense_trend = "descending"
            else:
                metrics.suspense_trend = "flat"

        # Quality flag analysis
        if len(pp_suspense) >= 6:
            middle_start = len(pp_suspense) // 3
            middle_end = 2 * len(pp_suspense) // 3
            middle_scores = pp_suspense[middle_start:middle_end]
            if max(middle_scores) - min(middle_scores) < 1.5:
                metrics.has_flat_middle = True

        if metrics.peak_position < 0.6:
            metrics.has_premature_peak = True

        # Check for sudden drops
        for i in range(1, len(pp_suspense)):
            if pp_suspense[i] < pp_suspense[i-1] - 2:
                metrics.has_sudden_drops = True
                break

    def _calculate_reader_metrics(
        self,
        metrics: StoryMetrics,
        evaluations: list[ReaderEvaluation],
        real_facts: Optional[CrimeFacts],
    ):
        """Calculate reader evaluation metrics.

        Args:
            metrics: Metrics object to update
            evaluations: Reader evaluations
            real_facts: Real crime facts
        """
        if not evaluations:
            return

        # Overall reader scores
        all_scores = [e.overall_score for e in evaluations]
        metrics.avg_reader_score = sum(all_scores) / len(all_scores)

        # Role-specific scores
        for eval in evaluations:
            if eval.reader_role == "logic_analyst":
                metrics.logic_score = eval.overall_score
            elif eval.reader_role == "intuitive_reader":
                metrics.engagement_score = eval.overall_score
            elif eval.reader_role == "genre_expert":
                metrics.genre_score = eval.overall_score

        # Criminal prediction accuracy
        if real_facts:
            correct_predictions = 0
            total_predictions = 0
            real_criminal = real_facts.criminal.name.lower()

            for eval in evaluations:
                for pred in eval.criminal_predictions.values():
                    if isinstance(pred, dict):
                        total_predictions += 1
                        if pred.get("prediction", "").lower() == real_criminal:
                            correct_predictions += 1
                            metrics.layer_leak_detected = True

            if total_predictions > 0:
                metrics.criminal_prediction_accuracy = correct_predictions / total_predictions

        # Issue counts
        for eval in evaluations:
            for flag in eval.inconsistency_flags:
                severity = flag.get("severity")
                if hasattr(severity, 'value'):
                    severity = severity.value
                if severity == "critical":
                    metrics.num_critical_issues += 1
                elif severity == "moderate":
                    metrics.num_moderate_issues += 1

    def format_metrics_table(self, metrics: StoryMetrics) -> str:
        """Format metrics as a readable table.

        Args:
            metrics: Story metrics

        Returns:
            Formatted table string
        """
        lines = [
            "=" * 60,
            "STORY EVALUATION METRICS",
            "=" * 60,
            "",
            "BASIC METRICS",
            "-" * 40,
            f"  Plot Points:                  {metrics.num_plot_points}",
            f"  Conspirator Interventions:    {metrics.num_conspirator_interventions}",
            f"  Obstacles:                    {metrics.num_obstacles}",
            "",
            "SUSPENSE METRICS",
            "-" * 40,
            f"  Average Suspense:             {metrics.avg_suspense:.2f} / 10",
            f"  Suspense Variance:            {metrics.suspense_variance:.2f}",
            f"  Suspense Trend:               {metrics.suspense_trend}",
            f"  Peak Suspense:                {metrics.peak_suspense:.2f}",
            f"  Peak Position:                {metrics.peak_position:.1%}",
            "",
            "DISCOVERY PATH METRICS",
            "-" * 40,
            f"  Initial Paths:                {metrics.initial_paths}",
            f"  Final Open Paths:             {metrics.final_paths}",
            f"  Paths Closed:                 {metrics.paths_closed}",
            f"  Close Rate (per plot point):  {metrics.path_close_rate:.2f}",
            "",
            "READER EVALUATION",
            "-" * 40,
            f"  Average Reader Score:         {metrics.avg_reader_score:.2f} / 10",
            f"  Logic Score:                  {metrics.logic_score:.2f}",
            f"  Engagement Score:             {metrics.engagement_score:.2f}",
            f"  Genre Score:                  {metrics.genre_score:.2f}",
            "",
            "DUAL-LAYER INTEGRITY",
            "-" * 40,
            f"  Layer Leak Detected:          {'YES' if metrics.layer_leak_detected else 'No'}",
            f"  Criminal Prediction Accuracy: {metrics.criminal_prediction_accuracy:.1%}",
            "",
            "QUALITY FLAGS",
            "-" * 40,
            f"  Flat Middle Section:          {'YES' if metrics.has_flat_middle else 'No'}",
            f"  Premature Peak:               {'YES' if metrics.has_premature_peak else 'No'}",
            f"  Sudden Drops:                 {'YES' if metrics.has_sudden_drops else 'No'}",
            f"  Critical Issues:              {metrics.num_critical_issues}",
            f"  Moderate Issues:              {metrics.num_moderate_issues}",
            "",
            "=" * 60,
            f"OVERALL QUALITY SCORE: {metrics.get_overall_score():.1f} / 100",
            "=" * 60,
        ]

        return "\n".join(lines)

    def compare_metrics(
        self,
        metrics_list: list[StoryMetrics],
        labels: list[str],
    ) -> str:
        """Compare multiple story metrics.

        Args:
            metrics_list: List of metrics to compare
            labels: Labels for each story

        Returns:
            Comparison table string
        """
        if not metrics_list:
            return "No metrics to compare"

        # Build comparison table
        header = ["Metric"] + labels
        rows = [
            ["Plot Points"] + [str(m.num_plot_points) for m in metrics_list],
            ["Avg Suspense"] + [f"{m.avg_suspense:.2f}" for m in metrics_list],
            ["Suspense Trend"] + [m.suspense_trend for m in metrics_list],
            ["Reader Score"] + [f"{m.avg_reader_score:.2f}" for m in metrics_list],
            ["Layer Leak"] + ["YES" if m.layer_leak_detected else "No" for m in metrics_list],
            ["Critical Issues"] + [str(m.num_critical_issues) for m in metrics_list],
            ["Overall Score"] + [f"{m.get_overall_score():.1f}" for m in metrics_list],
        ]

        # Format as table
        col_widths = [max(len(str(row[i])) for row in [header] + rows) + 2
                      for i in range(len(header))]

        lines = []
        lines.append("".join(h.ljust(w) for h, w in zip(header, col_widths)))
        lines.append("-" * sum(col_widths))
        for row in rows:
            lines.append("".join(str(c).ljust(w) for c, w in zip(row, col_widths)))

        return "\n".join(lines)
