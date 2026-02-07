#!/usr/bin/env python3
"""
Main story generation script for Smokemirror.

Usage:
    python scripts/generate_story.py [options]

Examples:
    python scripts/generate_story.py --crime-type murder --setting "tech startup"
    python scripts/generate_story.py --config configs/custom.yaml
    python scripts/generate_story.py --mock  # For testing without GPU
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config import load_config, Config
from src.models.llm_wrapper import create_llm_wrapper
from src.generators.crime_backstory import CrimeBackstoryGenerator
from src.generators.fabricated_narrative import FabricatedNarrativeGenerator
from src.generators.story_assembler import StoryAssembler
from src.controllers.suspense_meta_controller import SuspenseMetaController
from src.evaluation.reader_simulation import ReaderSimulator
from src.evaluation.feedback_aggregation import FeedbackAggregator
from src.evaluation.metrics import MetricsCalculator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a crime mystery story with Smokemirror"
    )

    # Configuration
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file (default: configs/default.yaml)"
    )

    # Story parameters
    parser.add_argument(
        "--crime-type",
        type=str,
        default=None,
        choices=["murder", "embezzlement", "art theft", "corporate sabotage", "kidnapping"],
        help="Type of crime for the story"
    )
    parser.add_argument(
        "--setting",
        type=str,
        default=None,
        help="Setting for the story (e.g., 'tech startup', 'law firm')"
    )
    parser.add_argument(
        "--num-conspirators",
        type=int,
        default=None,
        help="Number of conspirators (2-4)"
    )

    # Model parameters
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model name (e.g., 'Qwen/Qwen3-8B')"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock LLM for testing (no GPU required)"
    )

    # Generation parameters
    parser.add_argument(
        "--min-plot-points",
        type=int,
        default=None,
        help="Minimum number of plot points"
    )
    parser.add_argument(
        "--max-plot-points",
        type=int,
        default=None,
        help="Maximum number of plot points"
    )
    parser.add_argument(
        "--max-refinement-iterations",
        type=int,
        default=None,
        help="Maximum refinement iterations"
    )

    # Output parameters
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory for generated story"
    )
    parser.add_argument(
        "--no-refinement",
        action="store_true",
        help="Skip the refinement loop"
    )
    parser.add_argument(
        "--no-evaluation",
        action="store_true",
        help="Skip reader evaluation"
    )

    # Reproducibility
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility"
    )

    return parser.parse_args()


def apply_args_to_config(args, config: Config) -> Config:
    """Apply command line arguments to configuration."""
    if args.model:
        config.model.name = args.model
    if args.min_plot_points:
        config.generation.min_plot_points = args.min_plot_points
    if args.max_plot_points:
        config.generation.max_plot_points = args.max_plot_points
    if args.max_refinement_iterations:
        config.refinement.max_iterations = args.max_refinement_iterations
    if args.output_dir:
        config.output.output_dir = args.output_dir
    if args.seed:
        config.seed = args.seed

    return config


def save_outputs(
    output_dir: str,
    story_text: str,
    plot_points: list,
    real_facts,
    fabricated_facts,
    metrics,
    run_id: str,
):
    """Save all outputs to files."""
    os.makedirs(output_dir, exist_ok=True)

    # Save story
    story_path = os.path.join(output_dir, f"story_{run_id}.md")
    with open(story_path, "w") as f:
        f.write(story_text)
    logger.info(f"Story saved to {story_path}")

    # Save plot points
    plot_points_path = os.path.join(output_dir, f"plot_points_{run_id}.json")
    with open(plot_points_path, "w") as f:
        json.dump([pp.to_dict() for pp in plot_points], f, indent=2)
    logger.info(f"Plot points saved to {plot_points_path}")

    # Save facts
    facts_path = os.path.join(output_dir, f"facts_{run_id}.json")
    with open(facts_path, "w") as f:
        json.dump({
            "real_facts": real_facts.to_dict(),
            "fabricated_facts": fabricated_facts.to_dict(),
        }, f, indent=2)
    logger.info(f"Facts saved to {facts_path}")

    # Save metrics
    if metrics:
        metrics_path = os.path.join(output_dir, f"metrics_{run_id}.json")
        with open(metrics_path, "w") as f:
            json.dump(metrics.to_dict(), f, indent=2)
        logger.info(f"Metrics saved to {metrics_path}")


def main():
    """Main entry point."""
    args = parse_args()

    # Load configuration
    config = load_config(args.config)
    config = apply_args_to_config(args, config)
    config.set_seed()

    logger.info("=" * 60)
    logger.info("SMOKEMIRROR - Crime Mystery Story Generator")
    logger.info("=" * 60)
    logger.info(f"Model: {config.model.name}")
    logger.info(f"Min plot points: {config.generation.min_plot_points}")
    logger.info(f"Seed: {config.seed}")

    # Generate run ID
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Initialize LLM
    logger.info("\n[1/6] Initializing LLM...")
    llm = create_llm_wrapper(config.model, use_mock=args.mock)

    # Step 1: Generate crime backstory
    logger.info("\n[2/6] Generating crime backstory...")
    backstory_generator = CrimeBackstoryGenerator(llm, config.generation)
    real_facts, discovery_paths = backstory_generator.generate(
        crime_type=args.crime_type,
        setting=args.setting,
        num_conspirators=args.num_conspirators,
    )
    logger.info(f"Crime: {real_facts.crime_type}")
    logger.info(f"Criminal: {real_facts.criminal.name}")
    logger.info(f"Conspirators: {[c.name for c in real_facts.conspirators]}")
    logger.info(f"Discovery paths: {len(discovery_paths)}")

    # Step 2: Generate fabricated narrative
    logger.info("\n[3/6] Generating fabricated narrative...")
    fabricated_generator = FabricatedNarrativeGenerator(llm)
    fabricated_facts = fabricated_generator.generate(real_facts)
    logger.info(f"Fake suspect: {fabricated_facts.fake_suspect.name}")
    logger.info(f"Cover story: {fabricated_facts.cover_story[:100]}...")

    # Step 3: Generate detective story with suspense controller
    logger.info("\n[4/6] Generating detective investigation story...")
    meta_controller = SuspenseMetaController(
        llm, config.suspense, config.generation
    )
    plot_points, story_state = meta_controller.generate_story(
        real_facts, fabricated_facts, discovery_paths
    )
    logger.info(f"Generated {len(plot_points)} plot points")
    logger.info(f"Final open paths: {len(story_state.get_open_paths())}")

    # Step 4: Reader evaluation and refinement
    metrics = None
    if not args.no_evaluation:
        logger.info("\n[5/6] Running reader evaluation...")
        reader_simulator = ReaderSimulator(llm, config.reader_simulation)
        evaluations = reader_simulator.evaluate_story(plot_points, real_facts)

        if evaluations:
            # Calculate metrics
            metrics_calculator = MetricsCalculator()
            metrics = metrics_calculator.calculate(
                plot_points, story_state, evaluations, real_facts,
                initial_paths=len(discovery_paths)
            )
            logger.info(metrics_calculator.format_metrics_table(metrics))

            # Refinement loop
            if not args.no_refinement and config.refinement.max_iterations > 0:
                feedback_aggregator = FeedbackAggregator(config.refinement)
                directives = feedback_aggregator.aggregate(
                    evaluations, plot_points, real_facts
                )

                if directives:
                    logger.info(f"\nFound {len(directives)} issues to address")
                    logger.info(feedback_aggregator.get_revision_summary(directives))

                    # Apply revisions
                    critical_directives = feedback_aggregator.filter_directives(
                        directives, max_revisions=5
                    )
                    if critical_directives:
                        revision_targets = []
                        for d in critical_directives:
                            revision_targets.extend(d.target_plot_points)

                        plot_points = meta_controller.revise_plot_points(
                            plot_points,
                            list(set(revision_targets)),
                            [d.to_dict() for d in critical_directives],
                            real_facts,
                            fabricated_facts,
                        )
                        logger.info("Revisions applied")
    else:
        logger.info("\n[5/6] Skipping evaluation (--no-evaluation)")

    # Step 5: Assemble final story
    logger.info("\n[6/6] Assembling final narrative...")
    story_assembler = StoryAssembler(llm)
    story_text = story_assembler.assemble(
        plot_points, real_facts, fabricated_facts
    )

    # Save outputs
    save_outputs(
        config.output.output_dir,
        story_text,
        plot_points,
        real_facts,
        fabricated_facts,
        metrics,
        run_id,
    )

    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("GENERATION COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Story saved to: {config.output.output_dir}/story_{run_id}.md")
    if metrics:
        logger.info(f"Overall Quality Score: {metrics.get_overall_score():.1f}/100")
    logger.info("=" * 60)

    # Print story preview
    print("\n" + "=" * 60)
    print("STORY PREVIEW (first 2000 chars)")
    print("=" * 60)
    print(story_text[:2000])
    if len(story_text) > 2000:
        print("\n... [truncated] ...")

    return 0


if __name__ == "__main__":
    sys.exit(main())
