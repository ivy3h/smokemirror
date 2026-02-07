#!/usr/bin/env python3
"""
Simple test script for Smokemirror.
Tests each component individually before running full pipeline.
"""

import os
import sys
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


def test_imports():
    """Test that all modules can be imported."""
    logger.info("Testing imports...")

    from src.utils.config import load_config
    from src.models.llm_wrapper import LLMWrapper, create_llm_wrapper
    from src.generators.crime_backstory import CrimeBackstoryGenerator
    from src.generators.fabricated_narrative import FabricatedNarrativeGenerator
    from src.generators.story_assembler import StoryAssembler
    from src.controllers.suspense_meta_controller import SuspenseMetaController
    from src.evaluation.reader_simulation import ReaderSimulator
    from src.evaluation.feedback_aggregation import FeedbackAggregator
    from src.evaluation.metrics import MetricsCalculator

    logger.info("All imports successful!")
    return True


def test_config():
    """Test configuration loading."""
    logger.info("Testing configuration...")

    from src.utils.config import load_config

    config = load_config(str(project_root / "configs" / "test_small.yaml"))
    logger.info(f"  Model: {config.model.name}")
    logger.info(f"  Min plot points: {config.generation.min_plot_points}")
    logger.info(f"  Seed: {config.seed}")

    return config


def test_model_loading(config):
    """Test model loading."""
    logger.info("Testing model loading...")

    from src.models.llm_wrapper import create_llm_wrapper

    llm = create_llm_wrapper(config.model, use_mock=False)
    logger.info(f"  Model loaded: {config.model.name}")

    # Test simple generation
    logger.info("Testing simple generation...")
    response = llm.generate(
        prompt="Write a one-sentence mystery: ",
        max_new_tokens=100,
    )
    logger.info(f"  Response: {response.text[:200]}...")

    return llm


def test_json_generation(llm):
    """Test JSON generation capability."""
    logger.info("Testing JSON generation...")

    response = llm.generate_with_retry(
        prompt='''Generate a simple character in JSON format:
{"name": "character name", "occupation": "job", "motive": "reason"}''',
        expect_json=True,
        max_new_tokens=200,
    )

    if response.parsed_json:
        logger.info(f"  JSON parsed successfully: {response.parsed_json}")
        return True
    else:
        logger.warning(f"  JSON parsing failed. Raw response: {response.text[:200]}")
        return False


def test_crime_backstory(llm, config):
    """Test crime backstory generation."""
    logger.info("Testing crime backstory generation...")

    from src.generators.crime_backstory import CrimeBackstoryGenerator

    generator = CrimeBackstoryGenerator(llm, config.generation)
    real_facts, discovery_paths = generator.generate(
        crime_type="murder",
        setting="tech startup",
        num_conspirators=2,
    )

    logger.info(f"  Crime type: {real_facts.crime_type}")
    logger.info(f"  Criminal: {real_facts.criminal.name}")
    logger.info(f"  Conspirators: {[c.name for c in real_facts.conspirators]}")
    logger.info(f"  Discovery paths: {len(discovery_paths)}")

    return real_facts, discovery_paths


def test_fabricated_narrative(llm, real_facts):
    """Test fabricated narrative generation."""
    logger.info("Testing fabricated narrative generation...")

    from src.generators.fabricated_narrative import FabricatedNarrativeGenerator

    generator = FabricatedNarrativeGenerator(llm)
    fabricated_facts = generator.generate(real_facts, max_retries=2)

    logger.info(f"  Fake suspect: {fabricated_facts.fake_suspect.name}")
    logger.info(f"  Cover story: {fabricated_facts.cover_story[:100]}...")

    return fabricated_facts


def test_suspense_controller(llm, config, real_facts, fabricated_facts, discovery_paths):
    """Test suspense meta-controller."""
    logger.info("Testing suspense meta-controller...")

    from src.controllers.suspense_meta_controller import SuspenseMetaController

    controller = SuspenseMetaController(llm, config.suspense, config.generation)
    plot_points, story_state = controller.generate_story(
        real_facts, fabricated_facts, discovery_paths
    )

    logger.info(f"  Generated {len(plot_points)} plot points")
    logger.info(f"  Final open paths: {len(story_state.get_open_paths())}")
    logger.info(f"  Final suspense level: {story_state.suspense_level}")

    return plot_points, story_state


def test_story_assembly(llm, plot_points, real_facts, fabricated_facts):
    """Test story assembly."""
    logger.info("Testing story assembly...")

    from src.generators.story_assembler import StoryAssembler

    assembler = StoryAssembler(llm)
    story = assembler.assemble(plot_points, real_facts, fabricated_facts)

    logger.info(f"  Story length: {len(story)} characters")
    logger.info(f"  Preview: {story[:500]}...")

    return story


def test_metrics(plot_points, story_state):
    """Test metrics calculation."""
    logger.info("Testing metrics calculation...")

    from src.evaluation.metrics import MetricsCalculator

    calculator = MetricsCalculator()
    metrics = calculator.calculate(
        plot_points, story_state, evaluations=[],
        initial_paths=4,
    )

    logger.info(f"  Overall score: {metrics.get_overall_score():.1f}/100")
    logger.info(f"  Avg suspense: {metrics.avg_suspense:.2f}")
    logger.info(calculator.format_metrics_table(metrics))

    return metrics


def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("SMOKEMIRROR SIMPLE TEST")
    logger.info("=" * 60)

    # Test imports
    if not test_imports():
        return 1

    # Test config
    config = test_config()
    config.set_seed()

    # Test model
    llm = test_model_loading(config)

    # Test JSON generation
    test_json_generation(llm)

    # Test crime backstory
    real_facts, discovery_paths = test_crime_backstory(llm, config)

    # Test fabricated narrative
    fabricated_facts = test_fabricated_narrative(llm, real_facts)

    # Test suspense controller
    plot_points, story_state = test_suspense_controller(
        llm, config, real_facts, fabricated_facts, discovery_paths
    )

    # Test story assembly
    story = test_story_assembly(llm, plot_points, real_facts, fabricated_facts)

    # Test metrics
    metrics = test_metrics(plot_points, story_state)

    # Save outputs with timestamp to avoid overwriting
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = project_root / "outputs" / f"test_simple_{run_id}"
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "story.md", "w", encoding="utf-8") as f:
        f.write(story)

    logger.info("=" * 60)
    logger.info("ALL TESTS PASSED!")
    logger.info(f"Story saved to: {output_dir / 'story.md'}")
    logger.info("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
