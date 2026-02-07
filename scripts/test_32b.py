#!/usr/bin/env python3
"""
Test script for Smokemirror with Qwen3-32B model.
Uses thinking mode for better story generation quality.
"""

import os
import sys
import json
import logging
from datetime import datetime

# Set HuggingFace cache before imports
os.environ["HF_HOME"] = "/coc/pskynet6/jhe478/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/coc/pskynet6/jhe478/huggingface"

# Add project root to path
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Run full test with Qwen3-32B and thinking mode."""
    logger.info("=" * 60)
    logger.info("SMOKEMIRROR TEST - Qwen3-32B (Thinking Mode)")
    logger.info("=" * 60)

    # Import modules
    from src.utils.config import load_config
    from src.models.llm_wrapper import create_llm_wrapper
    from src.generators.crime_backstory import CrimeBackstoryGenerator
    from src.generators.fabricated_narrative import FabricatedNarrativeGenerator
    from src.generators.story_assembler import StoryAssembler
    from src.controllers.suspense_meta_controller import SuspenseMetaController
    from src.evaluation.metrics import MetricsCalculator

    # Load config
    config = load_config(str(project_root / "configs" / "test_32b.yaml"))
    config.set_seed()

    logger.info(f"Model: {config.model.name}")
    logger.info(f"Full precision (multi-GPU): {not config.model.load_in_4bit}")
    logger.info(f"Min plot points: {config.generation.min_plot_points}")
    logger.info(f"Thinking mode: ENABLED")

    # Initialize LLM
    logger.info("\n[1/6] Loading Qwen3-32B model (this may take a while)...")
    llm = create_llm_wrapper(config.model, use_mock=False)

    # Test basic generation with thinking
    logger.info("\nTesting basic generation with thinking mode...")
    response = llm.generate(
        prompt="Write a one-sentence mystery hook:",
        max_new_tokens=500,
    )
    # Show that thinking mode is working
    if "<think>" in response.text:
        logger.info("Thinking mode confirmed active")
    clean_response = llm._strip_thinking_tags(response.text)
    logger.info(f"Response: {clean_response[:300]}...")

    # Generate crime backstory
    logger.info("\n[2/6] Generating crime backstory...")
    backstory_gen = CrimeBackstoryGenerator(llm, config.generation)
    real_facts, discovery_paths = backstory_gen.generate(
        crime_type="murder",
        setting="prestigious art gallery during a private exhibition",
        num_conspirators=3,
    )
    logger.info(f"Crime: {real_facts.crime_type}")
    logger.info(f"Criminal: {real_facts.criminal.name}")
    logger.info(f"Victim: {real_facts.victim.name}")
    logger.info(f"Conspirators: {[c.name for c in real_facts.conspirators]}")
    logger.info(f"Discovery paths: {len(discovery_paths)}")

    # Generate fabricated narrative
    logger.info("\n[3/6] Generating fabricated narrative...")
    fab_gen = FabricatedNarrativeGenerator(llm)
    fabricated_facts = fab_gen.generate(real_facts)
    logger.info(f"Fake suspect: {fabricated_facts.fake_suspect.name}")
    logger.info(f"Cover story: {fabricated_facts.cover_story[:200]}...")

    # Generate story with suspense controller
    logger.info("\n[4/6] Generating investigation story...")
    controller = SuspenseMetaController(llm, config.suspense, config.generation)
    plot_points, story_state = controller.generate_story(
        real_facts, fabricated_facts, discovery_paths
    )
    logger.info(f"Generated {len(plot_points)} plot points")
    logger.info(f"Final open paths: {len(story_state.get_open_paths())}")

    # Print plot point summary
    logger.info("\nPlot Point Summary:")
    for pp in plot_points:
        collision_marker = "[COLLISION]" if pp.is_collision else ""
        logger.info(f"  {pp.id}: suspense={pp.suspense_level}, paths_closed={len(pp.paths_closed)} {collision_marker}")

    # Assemble story with thinking mode enabled
    logger.info("\n[5/6] Assembling final narrative (with thinking mode)...")
    assembler = StoryAssembler(llm, use_thinking=True)  # Enable thinking for 32B
    story = assembler.assemble(plot_points, real_facts, fabricated_facts)

    # Calculate metrics
    logger.info("\n[6/6] Calculating metrics...")
    metrics_calc = MetricsCalculator()
    metrics = metrics_calc.calculate(
        plot_points, story_state, evaluations=[],
        real_facts=real_facts,
        initial_paths=len(discovery_paths),
    )

    # Print metrics table
    print("\n" + metrics_calc.format_metrics_table(metrics))

    # Save outputs
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = project_root / "outputs" / f"test_32b_{run_id}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save story
    with open(output_dir / "story.md", "w", encoding="utf-8") as f:
        f.write(story)

    # Save plot points
    with open(output_dir / "plot_points.json", "w", encoding="utf-8") as f:
        json.dump([pp.to_dict() for pp in plot_points], f, indent=2, ensure_ascii=False)

    # Save facts
    with open(output_dir / "facts.json", "w", encoding="utf-8") as f:
        json.dump({
            "real_facts": real_facts.to_dict(),
            "fabricated_facts": fabricated_facts.to_dict(),
        }, f, indent=2, ensure_ascii=False)

    # Save metrics
    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics.to_dict(), f, indent=2, ensure_ascii=False)

    logger.info("\n" + "=" * 60)
    logger.info("TEST COMPLETED SUCCESSFULLY!")
    logger.info("=" * 60)
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Overall Score: {metrics.get_overall_score():.1f}/100")
    logger.info("=" * 60)

    # Print story preview
    print("\n" + "=" * 60)
    print("STORY PREVIEW (first 3000 chars)")
    print("=" * 60)
    print(story[:3000])
    if len(story) > 3000:
        print("\n... [truncated] ...")

    return 0


if __name__ == "__main__":
    sys.exit(main())
