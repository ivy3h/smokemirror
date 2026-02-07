"""
Feedback Aggregation Module

Synthesizes feedback from multiple reader evaluations into
prioritized revision directives.
"""

import logging
from collections import defaultdict
from typing import Optional

from ..data_structures.facts import (
    ReaderEvaluation,
    RevisionDirective,
    IssueSeverity,
    IssueType,
    PlotPoint,
    CrimeFacts,
)
from ..utils.config import RefinementConfig

logger = logging.getLogger(__name__)


class FeedbackAggregator:
    """Aggregates reader feedback into revision directives."""

    def __init__(self, config: RefinementConfig):
        """Initialize the aggregator.

        Args:
            config: Refinement configuration
        """
        self.config = config

    def aggregate(
        self,
        evaluations: list[ReaderEvaluation],
        plot_points: list[PlotPoint],
        real_facts: Optional[CrimeFacts] = None,
    ) -> list[RevisionDirective]:
        """Aggregate evaluations into revision directives.

        Args:
            evaluations: Reader evaluations
            plot_points: Story plot points
            real_facts: Real crime facts (for layer leak detection)

        Returns:
            Prioritized list of RevisionDirective objects
        """
        if not evaluations:
            return []

        directives = []

        # 1. Check for layer leaks (highest priority)
        layer_leak_directives = self._check_layer_leaks(evaluations, real_facts)
        directives.extend(layer_leak_directives)

        # 2. Aggregate inconsistency flags
        inconsistency_directives = self._aggregate_inconsistencies(evaluations)
        directives.extend(inconsistency_directives)

        # 3. Analyze suspense curve issues
        suspense_directives = self._analyze_suspense_issues(evaluations, plot_points)
        directives.extend(suspense_directives)

        # 4. Check engagement issues
        engagement_directives = self._analyze_engagement(evaluations, plot_points)
        directives.extend(engagement_directives)

        # Calculate priorities and sort
        for directive in directives:
            directive.priority = self._calculate_priority(directive)

        directives.sort(key=lambda d: d.priority, reverse=True)

        return directives

    def _check_layer_leaks(
        self,
        evaluations: list[ReaderEvaluation],
        real_facts: Optional[CrimeFacts],
    ) -> list[RevisionDirective]:
        """Check for readers who correctly identified the real criminal.

        Args:
            evaluations: Reader evaluations
            real_facts: Real crime facts

        Returns:
            List of layer leak directives
        """
        if real_facts is None:
            return []

        directives = []
        real_criminal = real_facts.criminal.name.lower()

        # Track which checkpoints had correct predictions
        leak_checkpoints = defaultdict(list)

        for eval in evaluations:
            for checkpoint, pred in eval.criminal_predictions.items():
                if isinstance(pred, dict):
                    prediction = pred.get("prediction", "").lower()
                    confidence = pred.get("confidence", "low")
                    reasoning = pred.get("reasoning", "")

                    if prediction == real_criminal:
                        leak_checkpoints[checkpoint].append({
                            "reader": eval.reader_role,
                            "confidence": confidence,
                            "reasoning": reasoning,
                        })

        for checkpoint, leaks in leak_checkpoints.items():
            if len(leaks) >= 1:  # Even one leak is critical
                # Find relevant plot points to revise
                try:
                    checkpoint_int = int(checkpoint)
                    # Revise plot points before this checkpoint
                    target_points = list(range(max(0, checkpoint_int - 3), checkpoint_int + 1))
                except (ValueError, TypeError):
                    target_points = [0, 1, 2]

                directives.append(RevisionDirective(
                    target_plot_points=target_points,
                    issue_type=IssueType.LAYER_LEAK,
                    severity=IssueSeverity.CRITICAL,
                    description=f"Reader(s) correctly identified real criminal at checkpoint {checkpoint}",
                    suggested_revision="Strengthen fabricated narrative, add more misdirection, or reduce clues pointing to real criminal",
                    consensus_count=len(leaks),
                    priority=0,  # Will be calculated later
                ))

        return directives

    def _aggregate_inconsistencies(
        self,
        evaluations: list[ReaderEvaluation],
    ) -> list[RevisionDirective]:
        """Aggregate inconsistency flags across readers.

        Args:
            evaluations: Reader evaluations

        Returns:
            List of inconsistency directives
        """
        # Group flags by plot point
        flags_by_point: dict[int, list[dict]] = defaultdict(list)

        for eval in evaluations:
            for flag in eval.inconsistency_flags:
                pp_id = flag.get("plot_point", 0)
                flags_by_point[pp_id].append({
                    "reader": eval.reader_role,
                    "issue": flag.get("issue", "Unknown"),
                    "severity": flag.get("severity", IssueSeverity.MINOR),
                })

        directives = []

        for pp_id, flags in flags_by_point.items():
            # Determine consensus count
            consensus_count = len(set(f["reader"] for f in flags))

            # Determine highest severity
            severities = [f["severity"] for f in flags]
            if IssueSeverity.CRITICAL in severities:
                severity = IssueSeverity.CRITICAL
            elif IssueSeverity.MODERATE in severities:
                severity = IssueSeverity.MODERATE
            else:
                severity = IssueSeverity.MINOR

            # Determine issue type
            issues_text = " ".join(f["issue"] for f in flags).lower()
            if "logic" in issues_text or "inconsisten" in issues_text or "contradict" in issues_text:
                issue_type = IssueType.LOGICAL_INCONSISTENCY
            elif "character" in issues_text or "behavior" in issues_text or "implausib" in issues_text:
                issue_type = IssueType.CHARACTER_IMPLAUSIBILITY
            elif "trope" in issues_text or "clich" in issues_text:
                issue_type = IssueType.TROPE_OVERUSE
            else:
                issue_type = IssueType.LOGICAL_INCONSISTENCY

            # Only create directive if consensus or critical
            if consensus_count >= self.config.consensus_threshold or severity == IssueSeverity.CRITICAL:
                directives.append(RevisionDirective(
                    target_plot_points=[pp_id],
                    issue_type=issue_type,
                    severity=severity,
                    description="; ".join(f["issue"] for f in flags),
                    suggested_revision=f"Address the {issue_type.value} at plot point {pp_id}",
                    consensus_count=consensus_count,
                    priority=0,
                ))

        return directives

    def _analyze_suspense_issues(
        self,
        evaluations: list[ReaderEvaluation],
        plot_points: list[PlotPoint],
    ) -> list[RevisionDirective]:
        """Analyze suspense curve for issues.

        Args:
            evaluations: Reader evaluations
            plot_points: Story plot points

        Returns:
            List of suspense-related directives
        """
        directives = []

        # Calculate average suspense curve
        all_scores: dict[int, list[float]] = defaultdict(list)
        for eval in evaluations:
            for pp_id, score in eval.suspense_scores.items():
                all_scores[pp_id].append(score)

        avg_curve = {
            pp_id: sum(scores) / len(scores)
            for pp_id, scores in all_scores.items()
        }

        if not avg_curve:
            return directives

        scores = [avg_curve[k] for k in sorted(avg_curve.keys())]

        # Check for flat middle section
        if len(scores) >= 6:
            middle_start = len(scores) // 3
            middle_end = 2 * len(scores) // 3
            middle_scores = scores[middle_start:middle_end]

            if max(middle_scores) - min(middle_scores) < 1.5:
                target_points = list(range(middle_start, middle_end))
                directives.append(RevisionDirective(
                    target_plot_points=target_points,
                    issue_type=IssueType.PACING_ISSUE,
                    severity=IssueSeverity.MODERATE,
                    description="Suspense plateaus in middle section",
                    suggested_revision="Add conspirator intervention or new threat to middle section",
                    consensus_count=len(evaluations),  # All readers see same curve
                    priority=0,
                ))

        # Check for sudden drops
        for i in range(1, len(scores)):
            if scores[i] < scores[i-1] - 2.0:
                directives.append(RevisionDirective(
                    target_plot_points=[i],
                    issue_type=IssueType.SUSPENSE_DROP,
                    severity=IssueSeverity.MODERATE,
                    description=f"Sharp suspense drop at plot point {i}",
                    suggested_revision="Revise to maintain tension; avoid giving detective too much information at once",
                    consensus_count=len(evaluations),
                    priority=0,
                ))

        # Check if overall suspense is too low
        avg_suspense = sum(scores) / len(scores)
        if avg_suspense < self.config.consensus_threshold + 2:  # Using threshold as reference
            directives.append(RevisionDirective(
                target_plot_points=list(range(len(scores))),
                issue_type=IssueType.PACING_ISSUE,
                severity=IssueSeverity.MODERATE,
                description=f"Overall suspense too low (average: {avg_suspense:.1f})",
                suggested_revision="Increase stakes, add more obstacles, or strengthen conspirator threats",
                consensus_count=len(evaluations),
                priority=0,
            ))

        return directives

    def _analyze_engagement(
        self,
        evaluations: list[ReaderEvaluation],
        plot_points: list[PlotPoint],
    ) -> list[RevisionDirective]:
        """Analyze engagement feedback.

        Args:
            evaluations: Reader evaluations
            plot_points: Story plot points

        Returns:
            List of engagement-related directives
        """
        directives = []

        # Find consistently least engaging plot points
        least_engaging_counts: dict[int, int] = defaultdict(int)

        for eval in evaluations:
            engagement = eval.engagement_assessment
            if isinstance(engagement, dict):
                for pp_id in engagement.get("least_engaging", []):
                    try:
                        least_engaging_counts[int(pp_id)] += 1
                    except (ValueError, TypeError):
                        pass

        # Flag plot points that multiple readers found unengaging
        for pp_id, count in least_engaging_counts.items():
            if count >= self.config.consensus_threshold:
                directives.append(RevisionDirective(
                    target_plot_points=[pp_id],
                    issue_type=IssueType.PACING_ISSUE,
                    severity=IssueSeverity.MINOR,
                    description=f"Plot point {pp_id} found unengaging by {count} readers",
                    suggested_revision="Add more tension, conflict, or interesting detail",
                    consensus_count=count,
                    priority=0,
                ))

        return directives

    def _calculate_priority(self, directive: RevisionDirective) -> float:
        """Calculate priority score for a directive.

        Args:
            directive: The revision directive

        Returns:
            Priority score (higher = more urgent)
        """
        # Base score from severity
        severity_scores = {
            IssueSeverity.CRITICAL: self.config.critical_issue_weight,
            IssueSeverity.MODERATE: self.config.moderate_issue_weight,
            IssueSeverity.MINOR: self.config.minor_issue_weight,
        }
        base_score = severity_scores.get(directive.severity, 1.0)

        # Multiply by consensus count
        consensus_multiplier = 1.0 + (directive.consensus_count - 1) * 0.5

        # Boost for layer leaks
        if directive.issue_type == IssueType.LAYER_LEAK:
            base_score *= 3.0

        return base_score * consensus_multiplier

    def get_revision_summary(
        self,
        directives: list[RevisionDirective],
    ) -> str:
        """Get a human-readable summary of revisions needed.

        Args:
            directives: List of revision directives

        Returns:
            Summary string
        """
        if not directives:
            return "No revisions needed."

        lines = ["Revision Summary:", "=" * 40]

        critical = [d for d in directives if d.severity == IssueSeverity.CRITICAL]
        moderate = [d for d in directives if d.severity == IssueSeverity.MODERATE]
        minor = [d for d in directives if d.severity == IssueSeverity.MINOR]

        if critical:
            lines.append(f"\nCRITICAL ISSUES ({len(critical)}):")
            for d in critical:
                lines.append(f"  - {d.description}")
                lines.append(f"    Target: Plot points {d.target_plot_points}")

        if moderate:
            lines.append(f"\nMODERATE ISSUES ({len(moderate)}):")
            for d in moderate:
                lines.append(f"  - {d.description}")

        if minor:
            lines.append(f"\nMINOR ISSUES ({len(minor)}):")
            for d in minor:
                lines.append(f"  - {d.description}")

        return "\n".join(lines)

    def filter_directives(
        self,
        directives: list[RevisionDirective],
        max_revisions: int = 5,
    ) -> list[RevisionDirective]:
        """Filter to most important directives.

        Args:
            directives: All directives
            max_revisions: Maximum number to return

        Returns:
            Filtered list of directives
        """
        # Always include critical issues
        critical = [d for d in directives if d.severity == IssueSeverity.CRITICAL]

        # Then add highest priority others up to limit
        remaining = max_revisions - len(critical)
        non_critical = [d for d in directives if d.severity != IssueSeverity.CRITICAL]
        non_critical.sort(key=lambda d: d.priority, reverse=True)

        return critical + non_critical[:remaining]
