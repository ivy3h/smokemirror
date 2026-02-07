#!/usr/bin/env python3
"""
Test script for Smokemirror with reader simulation.
Uses Qwen3-4B for story generation, then evaluates with two reader models:
- Qwen/Qwen2.5-7B-Instruct
- deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
"""

import os
import sys
import json
import logging
import gc
import torch
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


def unload_model(llm):
    """Unload model to free GPU memory."""
    if hasattr(llm, 'model'):
        del llm.model
    if hasattr(llm, 'tokenizer'):
        del llm.tokenizer
    del llm
    gc.collect()
    torch.cuda.empty_cache()
    logger.info("Model unloaded, GPU memory freed")


def evaluate_with_reader(reader_model_name: str, story: str, plot_points: list, real_facts, config) -> dict:
    """Evaluate story with a specific reader model."""
    from src.models.llm_wrapper import LLMWrapper
    from src.utils.config import ModelConfig

    logger.info(f"\nLoading reader model: {reader_model_name}")

    # Create model config for reader
    reader_config = ModelConfig(
        name=reader_model_name,
        device="auto",
        load_in_4bit=False,
        load_in_8bit=False,
        torch_dtype="bfloat16",
        max_new_tokens=1024,
        temperature=0.3,  # Lower temperature for more consistent evaluation
        top_p=0.9,
        do_sample=True,
    )

    # Load reader model
    reader_llm = LLMWrapper(reader_config)

    evaluations = []

    # Evaluate story at different checkpoints
    checkpoints = [5, 10, 15, len(plot_points)]

    for checkpoint in checkpoints:
        if checkpoint > len(plot_points):
            continue

        # Get story up to this checkpoint
        partial_plot_points = plot_points[:checkpoint]

        # Create evaluation prompt
        prompt = f"""You are a literary critic evaluating a mystery story.

The story so far has {checkpoint} plot points. Here is a summary of the narrative:

{_summarize_plot_points(partial_plot_points)}

Please evaluate this story on the following criteria (score 1-10 for each):

1. SUSPENSE: How well does the story build and maintain tension?
2. CONSISTENCY: Are there any logical inconsistencies or plot holes?
3. PACING: Is the story well-paced, neither too slow nor too rushed?
4. CHARACTER: Are the characters believable and their actions motivated?
5. MYSTERY: How engaging is the mystery itself?

Respond in JSON format:
{{"suspense": <score>, "consistency": <score>, "pacing": <score>, "character": <score>, "mystery": <score>, "overall": <average>, "comments": "<brief feedback>"}}"""

        response = reader_llm.generate_with_retry(
            prompt=prompt,
            expect_json=True,
            max_new_tokens=500,
        )

        if response.parsed_json:
            eval_result = response.parsed_json
            eval_result["checkpoint"] = checkpoint
            eval_result["reader_model"] = reader_model_name
            evaluations.append(eval_result)
            logger.info(f"  Checkpoint {checkpoint}: overall={eval_result.get('overall', 'N/A')}")
        else:
            logger.warning(f"  Checkpoint {checkpoint}: Failed to parse evaluation")

    # Final overall evaluation
    final_prompt = f"""You are a literary critic giving a final evaluation of a complete mystery story.

The story has {len(plot_points)} plot points total.

Story preview:
{story[:3000]}

Please provide your final assessment:
1. Overall quality score (1-10)
2. Strengths of the story
3. Weaknesses or areas for improvement
4. Would you recommend this story to readers? (yes/no)

Respond in JSON format:
{{"final_score": <score>, "strengths": ["<strength1>", "<strength2>"], "weaknesses": ["<weakness1>", "<weakness2>"], "recommendation": "<yes/no>", "summary": "<one sentence summary>"}}"""

    final_response = reader_llm.generate_with_retry(
        prompt=final_prompt,
        expect_json=True,
        max_new_tokens=800,
    )

    final_eval = {}
    if final_response.parsed_json:
        final_eval = final_response.parsed_json
        final_eval["reader_model"] = reader_model_name
        logger.info(f"  Final score: {final_eval.get('final_score', 'N/A')}/10")

    # Unload reader model
    unload_model(reader_llm)

    return {
        "model": reader_model_name,
        "checkpoint_evaluations": evaluations,
        "final_evaluation": final_eval,
    }


def _summarize_plot_points(plot_points: list) -> str:
    """Create a summary of plot points."""
    summaries = []
    for i, pp in enumerate(plot_points, 1):
        collision_marker = " [NEAR DISCOVERY]" if pp.is_collision else ""
        summaries.append(f"{i}. {pp.detective_action[:100]}...{collision_marker}")
    return "\n".join(summaries)


def main():
    """Run full test with reader simulation."""
    logger.info("=" * 60)
    logger.info("SMOKEMIRROR TEST WITH READER SIMULATION")
    logger.info("=" * 60)

    # Reader models to use
    READER_MODELS = [
        "Qwen/Qwen2.5-7B-Instruct",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    ]

    # Import modules
    from src.utils.config import load_config
    from src.models.llm_wrapper import create_llm_wrapper
    from src.generators.crime_backstory import CrimeBackstoryGenerator
    from src.generators.fabricated_narrative import FabricatedNarrativeGenerator
    from src.generators.story_assembler import StoryAssembler
    from src.controllers.suspense_meta_controller import SuspenseMetaController
    from src.evaluation.metrics import MetricsCalculator

    # Load config
    config = load_config(str(project_root / "configs" / "test_4b.yaml"))
    config.set_seed()

    logger.info(f"Story generation model: {config.model.name}")
    logger.info(f"Reader models: {READER_MODELS}")

    # ========== PHASE 1: Generate Story with Qwen3-4B ==========
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 1: STORY GENERATION")
    logger.info("=" * 60)

    logger.info("\n[1/6] Loading Qwen3-4B model...")
    llm = create_llm_wrapper(config.model, use_mock=False)

    # Generate crime backstory
    logger.info("\n[2/6] Generating crime backstory...")
    backstory_gen = CrimeBackstoryGenerator(llm, config.generation)
    real_facts, discovery_paths = backstory_gen.generate(
        crime_type="murder",
        setting="luxury hotel",
        num_conspirators=2,
    )
    logger.info(f"Crime: {real_facts.crime_type}")
    logger.info(f"Criminal: {real_facts.criminal.name}")
    logger.info(f"Conspirators: {[c.name for c in real_facts.conspirators]}")

    # Generate fabricated narrative
    logger.info("\n[3/6] Generating fabricated narrative...")
    fab_gen = FabricatedNarrativeGenerator(llm)
    fabricated_facts = fab_gen.generate(real_facts)
    logger.info(f"Fake suspect: {fabricated_facts.fake_suspect.name}")

    # Generate story with suspense controller
    logger.info("\n[4/6] Generating investigation story...")
    controller = SuspenseMetaController(llm, config.suspense, config.generation)
    plot_points, story_state = controller.generate_story(
        real_facts, fabricated_facts, discovery_paths
    )
    logger.info(f"Generated {len(plot_points)} plot points")

    # Assemble story
    logger.info("\n[5/6] Assembling final narrative...")
    assembler = StoryAssembler(llm)
    story = assembler.assemble(plot_points, real_facts, fabricated_facts)
    story = llm._strip_thinking_tags(story)

    # Unload story generation model to free memory
    logger.info("\n[6/6] Unloading story generation model...")
    unload_model(llm)

    # ========== PHASE 2: Reader Evaluation ==========
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 2: READER EVALUATION")
    logger.info("=" * 60)

    all_reader_evaluations = []

    for reader_model in READER_MODELS:
        logger.info(f"\n--- Evaluating with {reader_model} ---")
        eval_result = evaluate_with_reader(
            reader_model, story, plot_points, real_facts, config
        )
        all_reader_evaluations.append(eval_result)

    # ========== PHASE 3: Calculate Final Metrics ==========
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 3: FINAL METRICS")
    logger.info("=" * 60)

    # Calculate base metrics
    metrics_calc = MetricsCalculator()
    metrics = metrics_calc.calculate(
        plot_points, story_state, evaluations=[],
        real_facts=real_facts,
        initial_paths=len(discovery_paths),
    )

    # Calculate average reader scores
    reader_scores = []
    for eval_result in all_reader_evaluations:
        if eval_result.get("final_evaluation", {}).get("final_score"):
            reader_scores.append(eval_result["final_evaluation"]["final_score"])

    avg_reader_score = sum(reader_scores) / len(reader_scores) if reader_scores else 0

    # Update metrics with reader scores
    metrics.avg_reader_score = avg_reader_score

    # Print metrics table
    print("\n" + metrics_calc.format_metrics_table(metrics))

    # Print reader evaluation summary
    print("\n" + "=" * 60)
    print("READER EVALUATION SUMMARY")
    print("=" * 60)
    for eval_result in all_reader_evaluations:
        model_name = eval_result["model"].split("/")[-1]
        final_eval = eval_result.get("final_evaluation", {})
        print(f"\n{model_name}:")
        print(f"  Final Score: {final_eval.get('final_score', 'N/A')}/10")
        print(f"  Recommendation: {final_eval.get('recommendation', 'N/A')}")
        if final_eval.get("summary"):
            print(f"  Summary: {final_eval['summary']}")

    # ========== Save Outputs ==========
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = project_root / "outputs" / f"test_readers_{run_id}"
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

    # Save reader evaluations
    with open(output_dir / "reader_evaluations.json", "w", encoding="utf-8") as f:
        json.dump(all_reader_evaluations, f, indent=2, ensure_ascii=False)

    logger.info("\n" + "=" * 60)
    logger.info("TEST COMPLETED SUCCESSFULLY!")
    logger.info("=" * 60)
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Overall Score: {metrics.get_overall_score():.1f}/100")
    logger.info(f"Average Reader Score: {avg_reader_score:.1f}/10")
    logger.info("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
