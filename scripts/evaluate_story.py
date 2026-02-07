#!/usr/bin/env python3
"""
Story evaluation script for Smokemirror.

Evaluates a previously generated story and outputs detailed metrics.

Usage:
    python scripts/evaluate_story.py --story-dir outputs/story_20240101_120000
    python scripts/evaluate_story.py --plot-points plot_points.json --facts facts.json
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config import load_config
from src.models.llm_wrapper import create_llm_wrapper
from src.data_structures.facts import (
    Character, CharacterRole, Evidence, EvidenceType,
    Timeline, CrimeFacts, FabricatedFacts, PlotPoint, StoryState, DiscoveryPath
)
from src.evaluation.reader_simulation import ReaderSimulator
from src.evaluation.feedback_aggregation import FeedbackAggregator
from src.evaluation.metrics import MetricsCalculator, StoryMetrics

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Evaluate a generated story"
    )

    parser.add_argument(
        "--story-dir",
        type=str,
        help="Directory containing story files"
    )
    parser.add_argument(
        "--plot-points",
        type=str,
        help="Path to plot points JSON file"
    )
    parser.add_argument(
        "--facts",
        type=str,
        help="Path to facts JSON file"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock LLM for testing"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file for metrics (JSON)"
    )

    return parser.parse_args()


def load_plot_points(path: str) -> list[PlotPoint]:
    """Load plot points from JSON file."""
    with open(path) as f:
        data = json.load(f)

    plot_points = []
    for pp_data in data:
        pp = PlotPoint(
            id=pp_data.get("id", len(plot_points)),
            description=pp_data.get("description", ""),
            detective_action=pp_data.get("detective_action"),
            conspirator_intervention=pp_data.get("conspirator_intervention"),
            obstacle=pp_data.get("obstacle"),
            reader_revelation=pp_data.get("reader_revelation"),
            detective_learns=pp_data.get("detective_learns"),
            paths_closed=pp_data.get("paths_closed", []),
            suspense_level=pp_data.get("suspense_level", 5),
            is_collision=pp_data.get("is_collision", False),
        )
        plot_points.append(pp)

    return plot_points


def load_facts(path: str) -> tuple[CrimeFacts, FabricatedFacts]:
    """Load facts from JSON file."""
    with open(path) as f:
        data = json.load(f)

    # Parse real facts
    real_data = data.get("real_facts", {})

    victim = Character(
        name=real_data.get("victim", {}).get("name", "Unknown"),
        role=CharacterRole.VICTIM,
        occupation=real_data.get("victim", {}).get("occupation", "Unknown"),
    )

    criminal = Character(
        name=real_data.get("criminal", {}).get("name", "Unknown"),
        role=CharacterRole.CRIMINAL,
        occupation=real_data.get("criminal", {}).get("occupation", "Unknown"),
        motive=real_data.get("criminal", {}).get("motive"),
    )

    conspirators = []
    for c_data in real_data.get("conspirators", []):
        conspirators.append(Character(
            name=c_data.get("name", "Unknown"),
            role=CharacterRole.CONSPIRATOR,
            occupation=c_data.get("occupation", "Unknown"),
            is_conspirator=True,
        ))

    timeline = Timeline()
    for event in real_data.get("timeline", {}).get("events", []):
        timeline.add_event(
            event.get("time", ""),
            event.get("description", ""),
            event.get("actor", ""),
            event.get("location", ""),
        )

    evidence = []
    for e_data in real_data.get("evidence", []):
        evidence.append(Evidence(
            id=e_data.get("id", f"E{len(evidence)}"),
            description=e_data.get("description", ""),
            evidence_type=EvidenceType.PHYSICAL,
            location=e_data.get("location", ""),
        ))

    real_facts = CrimeFacts(
        crime_type=real_data.get("crime_type", "unknown"),
        victim=victim,
        criminal=criminal,
        conspirators=conspirators,
        motive=real_data.get("motive", "Unknown"),
        method=real_data.get("method", "Unknown"),
        timeline=timeline,
        evidence=evidence,
        location=real_data.get("location", "Unknown"),
        coordination_plan=real_data.get("coordination_plan", "Unknown"),
    )

    # Parse fabricated facts
    fab_data = data.get("fabricated_facts", {})

    fake_suspect = Character(
        name=fab_data.get("fake_suspect", {}).get("name", "Unknown"),
        role=CharacterRole.SUSPECT,
        occupation=fab_data.get("fake_suspect", {}).get("occupation", "Unknown"),
    )

    fake_timeline = Timeline()
    for event in fab_data.get("fake_timeline", {}).get("events", []):
        fake_timeline.add_event(
            event.get("time", ""),
            event.get("description", ""),
            event.get("actor", ""),
            event.get("location", ""),
        )

    planted_evidence = []
    for e_data in fab_data.get("planted_evidence", []):
        planted_evidence.append(Evidence(
            id=e_data.get("id", f"PE{len(planted_evidence)}"),
            description=e_data.get("description", ""),
            evidence_type=EvidenceType.PHYSICAL,
            location=e_data.get("location", ""),
            is_planted=True,
        ))

    fabricated_facts = FabricatedFacts(
        fake_suspect=fake_suspect,
        fake_motive=fab_data.get("fake_motive", "Unknown"),
        fake_method=fab_data.get("fake_method", "Unknown"),
        fake_timeline=fake_timeline,
        planted_evidence=planted_evidence,
        alibis=fab_data.get("alibis", {}),
        cover_story=fab_data.get("cover_story", "Unknown"),
    )

    return real_facts, fabricated_facts


def main():
    """Main entry point."""
    args = parse_args()

    # Determine file paths
    if args.story_dir:
        story_dir = args.story_dir
        # Find files in directory
        files = os.listdir(story_dir)
        plot_points_file = next((f for f in files if f.startswith("plot_points")), None)
        facts_file = next((f for f in files if f.startswith("facts")), None)

        if not plot_points_file or not facts_file:
            logger.error("Could not find required files in story directory")
            return 1

        plot_points_path = os.path.join(story_dir, plot_points_file)
        facts_path = os.path.join(story_dir, facts_file)
    else:
        plot_points_path = args.plot_points
        facts_path = args.facts

    if not plot_points_path or not facts_path:
        logger.error("Must specify either --story-dir or both --plot-points and --facts")
        return 1

    # Load configuration
    config = load_config(args.config)

    logger.info("=" * 60)
    logger.info("SMOKEMIRROR - Story Evaluation")
    logger.info("=" * 60)

    # Load data
    logger.info("Loading story data...")
    plot_points = load_plot_points(plot_points_path)
    real_facts, fabricated_facts = load_facts(facts_path)

    logger.info(f"Loaded {len(plot_points)} plot points")
    logger.info(f"Crime type: {real_facts.crime_type}")
    logger.info(f"Criminal: {real_facts.criminal.name}")

    # Initialize LLM for reader simulation
    logger.info("\nInitializing LLM for evaluation...")
    llm = create_llm_wrapper(config.model, use_mock=args.mock)

    # Run reader simulation
    logger.info("\nRunning reader simulation...")
    reader_simulator = ReaderSimulator(llm, config.reader_simulation)
    evaluations = reader_simulator.evaluate_story(plot_points, real_facts)

    # Aggregate feedback
    logger.info("\nAggregating feedback...")
    feedback_aggregator = FeedbackAggregator(config.refinement)
    directives = feedback_aggregator.aggregate(evaluations, plot_points, real_facts)

    # Calculate metrics
    logger.info("\nCalculating metrics...")

    # Create a minimal story state
    story_state = StoryState()
    story_state.plot_points = plot_points
    story_state.discovery_paths = [DiscoveryPath(
        id=f"path_{i}",
        description=f"Discovery path {i}",
        is_open=(i < 2)  # Assume most paths closed
    ) for i in range(5)]

    metrics_calculator = MetricsCalculator()
    metrics = metrics_calculator.calculate(
        plot_points, story_state, evaluations, real_facts,
        initial_paths=5
    )

    # Print results
    print("\n" + metrics_calculator.format_metrics_table(metrics))

    # Print feedback summary
    if directives:
        print("\n" + feedback_aggregator.get_revision_summary(directives))

    # Analyze suspense curve
    suspense_curve = reader_simulator.get_suspense_curve(evaluations)
    curve_analysis = reader_simulator.analyze_suspense_curve(suspense_curve)

    print("\n" + "=" * 60)
    print("SUSPENSE CURVE ANALYSIS")
    print("=" * 60)
    print(f"Overall trend: {curve_analysis.get('trend', 'unknown')}")
    print(f"Average suspense: {curve_analysis.get('average', 0):.2f}")
    print(f"Peak position: {curve_analysis.get('peak_position', 0)}")

    if curve_analysis.get("issues"):
        print("\nIdentified issues:")
        for issue in curve_analysis["issues"]:
            print(f"  - {issue['type']}: {issue['description']}")

    # Save metrics if output specified
    if args.output:
        output_data = {
            "metrics": metrics.to_dict(),
            "overall_score": metrics.get_overall_score(),
            "suspense_curve": suspense_curve,
            "curve_analysis": curve_analysis,
            "num_directives": len(directives),
        }
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        logger.info(f"\nMetrics saved to {args.output}")

    print("\n" + "=" * 60)
    print(f"FINAL SCORE: {metrics.get_overall_score():.1f} / 100")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
