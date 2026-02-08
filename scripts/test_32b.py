#!/usr/bin/env python3
"""
Test script for Smokemirror with Qwen3-32B model.
Uses thinking mode for better story generation quality.
Includes full pipeline logging and reader simulation.
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
    """Run full test with Qwen3-32B, thinking mode, and reader simulation."""
    logger.info("=" * 60)
    logger.info("SMOKEMIRROR TEST - Qwen3-32B (Full Pipeline)")
    logger.info("=" * 60)

    # Import modules
    from src.utils.config import load_config, ModelConfig
    from src.models.llm_wrapper import create_llm_wrapper, LLMWrapper
    from src.generators.crime_backstory import CrimeBackstoryGenerator
    from src.generators.fabricated_narrative import FabricatedNarrativeGenerator
    from src.generators.story_assembler import StoryAssembler
    from src.controllers.suspense_meta_controller import SuspenseMetaController
    from src.evaluation.reader_simulation import ReaderSimulator
    from src.evaluation.metrics import MetricsCalculator
    from src.utils.pipeline_logger import PipelineLogger

    # Load config
    config = load_config(str(project_root / "configs" / "test_32b.yaml"))
    config.set_seed()

    # Setup output directory early for pipeline logging
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = project_root / "outputs" / f"test_32b_{run_id}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize pipeline logger
    pipeline_logger = PipelineLogger(output_dir, run_id)

    logger.info(f"Model: {config.model.name}")
    logger.info(f"Full precision (multi-GPU): {not config.model.load_in_4bit}")
    logger.info(f"Min plot points: {config.generation.min_plot_points}")
    logger.info(f"Thinking mode: ENABLED")
    logger.info(f"Reader simulation: {config.reader_simulation.enabled}")
    logger.info(f"Reader model: {config.reader_simulation.reader_model}")
    logger.info(f"Output directory: {output_dir}")

    # Log config
    pipeline_logger.log_step(
        step_name="config",
        step_type="initialization",
        output_data={
            "model": config.model.name,
            "reader_model": config.reader_simulation.reader_model,
            "min_plot_points": config.generation.min_plot_points,
            "max_plot_points": config.generation.max_plot_points,
            "reader_simulation_enabled": config.reader_simulation.enabled,
        }
    )

    # Initialize main LLM (story generation)
    logger.info("\n[1/7] Loading Qwen3-32B model (this may take a while)...")
    llm = create_llm_wrapper(config.model, use_mock=False)

    # Test basic generation with thinking
    logger.info("\nTesting basic generation with thinking mode...")
    test_prompt = "Write a one-sentence mystery hook:"
    response = llm.generate(
        prompt=test_prompt,
        max_new_tokens=500,
    )
    # Show that thinking mode is working
    if "<think>" in response.text:
        logger.info("Thinking mode confirmed active")
    clean_response = llm._strip_thinking_tags(response.text)
    logger.info(f"Response: {clean_response[:300]}...")

    pipeline_logger.log_prompt_response(
        section="test_generation",
        prompt=test_prompt,
        response=response.text,
        parsed_output={"clean_response": clean_response[:500]},
    )

    # Initialize reader LLM (separate smaller model for evaluation)
    reader_llm = None
    if config.reader_simulation.enabled:
        logger.info(f"\n[2/7] Loading reader model: {config.reader_simulation.reader_model}...")
        reader_model_config = ModelConfig(
            name=config.reader_simulation.reader_model,
            device="auto",
            load_in_4bit=False,
            load_in_8bit=False,
            torch_dtype="bfloat16",
            max_new_tokens=2048,
            temperature=0.3,  # Lower temperature for evaluation
            top_p=0.9,
            do_sample=True,
        )
        reader_llm = LLMWrapper(reader_model_config)
        logger.info("Reader model loaded successfully")
    else:
        logger.info("\n[2/7] Reader simulation disabled, skipping reader model...")

    # Generate crime backstory
    logger.info("\n[3/7] Generating crime backstory...")
    backstory_gen = CrimeBackstoryGenerator(llm, config.generation)

    # We'll capture the prompts by wrapping the generation
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

    pipeline_logger.log_step(
        step_name="crime_backstory",
        step_type="generation",
        output_data={
            "crime_type": real_facts.crime_type,
            "criminal": real_facts.criminal.name,
            "victim": real_facts.victim.name,
            "motive": real_facts.motive,
            "method": real_facts.method,
            "conspirators": [c.name for c in real_facts.conspirators],
            "num_discovery_paths": len(discovery_paths),
            "discovery_paths": [{"id": p.id, "description": p.description} for p in discovery_paths],
        }
    )

    # Generate fabricated narrative
    logger.info("\n[4/7] Generating fabricated narrative...")
    fab_gen = FabricatedNarrativeGenerator(llm)
    fabricated_facts = fab_gen.generate(real_facts)
    logger.info(f"Fake suspect: {fabricated_facts.fake_suspect.name}")
    logger.info(f"Cover story: {fabricated_facts.cover_story[:200]}...")

    pipeline_logger.log_step(
        step_name="fabricated_narrative",
        step_type="generation",
        output_data={
            "fake_suspect": fabricated_facts.fake_suspect.name,
            "cover_story": fabricated_facts.cover_story,
            "fake_motive": fabricated_facts.fake_motive,
            "fake_method": fabricated_facts.fake_method,
        }
    )

    # Generate story with suspense controller
    logger.info("\n[5/7] Generating investigation story...")
    controller = SuspenseMetaController(llm, config.suspense, config.generation)
    plot_points, story_state = controller.generate_story(
        real_facts, fabricated_facts, discovery_paths
    )
    logger.info(f"Generated {len(plot_points)} plot points")
    logger.info(f"Final open paths: {len(story_state.get_open_paths())}")

    # Log each plot point
    for pp in plot_points:
        collision_marker = "[COLLISION]" if pp.is_collision else ""
        logger.info(f"  {pp.id}: suspense={pp.suspense_level}, paths_closed={len(pp.paths_closed)} {collision_marker}")

        pipeline_logger.log_step(
            step_name=f"plot_point_{pp.id}",
            step_type="plot_generation",
            output_data=pp.to_dict(),
            is_collision=pp.is_collision,
            suspense_level=pp.suspense_level,
        )

    # Assemble story with thinking mode enabled
    logger.info("\n[6/7] Assembling final narrative (with thinking mode)...")
    assembler = StoryAssembler(llm, use_thinking=True)
    story = assembler.assemble(plot_points, real_facts, fabricated_facts)

    pipeline_logger.log_step(
        step_name="story_assembly",
        step_type="generation",
        output_data={
            "story_length": len(story),
            "word_count": len(story.split()),
        }
    )

    # Run reader simulation
    evaluations = []
    if config.reader_simulation.enabled and reader_llm:
        logger.info("\n[7/7] Running reader simulation...")
        reader_sim = ReaderSimulator(reader_llm, config.reader_simulation)

        evaluations = reader_sim.evaluate_story(plot_points, real_facts)

        # Log each reader evaluation
        for i, eval_result in enumerate(evaluations):
            logger.info(f"  Reader {i+1} ({eval_result.reader_role}): score={eval_result.overall_score:.2f}")
            logger.info(f"    Suspense scores: avg={sum(eval_result.suspense_scores.values())/len(eval_result.suspense_scores) if eval_result.suspense_scores else 0:.2f}")
            logger.info(f"    Inconsistency flags: {len(eval_result.inconsistency_flags)}")
            logger.info(f"    Criminal predictions: {len(eval_result.criminal_predictions)}")

            pipeline_logger.log_step(
                step_name=f"reader_eval_{eval_result.reader_role}",
                step_type="evaluation",
                output_data={
                    "reader_role": eval_result.reader_role,
                    "overall_score": eval_result.overall_score,
                    "suspense_scores": eval_result.suspense_scores,
                    "criminal_predictions": eval_result.criminal_predictions,
                    "inconsistency_flags": [
                        {"plot_point": f["plot_point"], "issue": f["issue"], "severity": f["severity"].value}
                        for f in eval_result.inconsistency_flags
                    ],
                    "engagement_assessment": eval_result.engagement_assessment,
                }
            )

        # Get suspense curve analysis
        suspense_curve = reader_sim.get_suspense_curve(evaluations)
        curve_analysis = reader_sim.analyze_suspense_curve(suspense_curve)
        logger.info(f"\nSuspense curve analysis:")
        logger.info(f"  Trend: {curve_analysis['trend']}")
        logger.info(f"  Peak position: {curve_analysis['peak_position']}")
        logger.info(f"  Average: {curve_analysis['average']:.2f}")
        logger.info(f"  Issues: {len(curve_analysis['issues'])}")

        # Check for layer leak
        layer_leak = reader_sim.check_layer_leak(evaluations, real_facts)
        logger.info(f"  Layer leak detected: {layer_leak}")

        pipeline_logger.log_step(
            step_name="suspense_curve_analysis",
            step_type="analysis",
            output_data={
                "suspense_curve": suspense_curve,
                "curve_analysis": curve_analysis,
                "layer_leak_detected": layer_leak,
            }
        )
    else:
        logger.info("\n[7/7] Skipping reader simulation (disabled or no reader model)...")

    # Calculate metrics
    logger.info("\nCalculating metrics...")
    metrics_calc = MetricsCalculator()
    metrics = metrics_calc.calculate(
        plot_points, story_state, evaluations,
        real_facts=real_facts,
        initial_paths=len(discovery_paths),
    )

    # Print metrics table
    print("\n" + metrics_calc.format_metrics_table(metrics))

    pipeline_logger.log_step(
        step_name="metrics_calculation",
        step_type="analysis",
        output_data=metrics.to_dict(),
    )

    # Save all outputs
    logger.info("\nSaving outputs...")

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

    # Save reader evaluations
    if evaluations:
        eval_data = []
        for eval_result in evaluations:
            eval_data.append({
                "reader_role": eval_result.reader_role,
                "overall_score": eval_result.overall_score,
                "suspense_scores": eval_result.suspense_scores,
                "criminal_predictions": eval_result.criminal_predictions,
                "inconsistency_flags": [
                    {"plot_point": f["plot_point"], "issue": f["issue"], "severity": f["severity"].value}
                    for f in eval_result.inconsistency_flags
                ],
                "engagement_assessment": eval_result.engagement_assessment,
            })
        pipeline_logger.save_reader_evaluations(eval_data)

    # Save pipeline logs
    pipeline_logger.save_summary()
    pipeline_logger.save_full_log()

    logger.info("\n" + "=" * 60)
    logger.info("TEST COMPLETED SUCCESSFULLY!")
    logger.info("=" * 60)
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Overall Score: {metrics.get_overall_score():.1f}/100")
    logger.info("=" * 60)
    logger.info("\nSaved files:")
    logger.info(f"  - story.md (final story)")
    logger.info(f"  - plot_points.json (plot structure)")
    logger.info(f"  - facts.json (real + fabricated facts)")
    logger.info(f"  - metrics.json (evaluation metrics)")
    if evaluations:
        logger.info(f"  - reader_evaluations.json (reader feedback)")
    logger.info(f"  - pipeline_logs/ (intermediate steps)")
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
