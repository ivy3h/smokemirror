# Smokemirror

A crime mystery story generation system powered by local LLMs. Smokemirror creates narratives with a **dual-layer deception** structure: the reader knows the truth from the start, while the detective is systematically misled by conspirators — producing dramatic irony and suspense.

## Features

- **Dual-Layer Narrative**: Reader sees the real crime (prologue) while the detective chases fabricated leads
- **Suspense Meta-Controller**: Iteratively generates plot points with collision detection, discovery path management, and countdown mechanics
- **Reader Simulation**: Simulated readers (logic analyst, intuitive reader, genre expert) evaluate story quality and flag issues
- **Refinement Loop**: Automatically revises plot points based on reader feedback
- **Multiple Model Support**: Works with Qwen3, Qwen2.5, Llama, Mistral, Gemma, or any HuggingFace causal LM

## Project Structure

```
smokemirror/
├── configs/                    # YAML configuration files
│   ├── default.yaml           #   Qwen3-8B (4-bit quantization)
│   ├── test_4b.yaml           #   Qwen3-4B (no quantization)
│   ├── test_32b.yaml          #   Qwen3-32B (multi-GPU)
│   └── test_qwen25_7b.yaml   #   Qwen2.5-7B-Instruct
├── scripts/                    # Entry points
│   ├── generate_story.py      #   Main generation pipeline
│   ├── generate_free.py       #   Simplified generation
│   ├── generate_dual_detective.py  # Alternative narrative format
│   ├── evaluate_story.py      #   Standalone evaluation
│   └── translate_story.py     #   Chinese translation
├── src/
│   ├── models/
│   │   └── llm_wrapper.py     # LLM interface (HuggingFace transformers)
│   ├── generators/
│   │   ├── crime_backstory.py       # Real crime facts
│   │   ├── fabricated_narrative.py  # False narrative for detective
│   │   └── story_assembler.py      # Plot points → prose chapters
│   ├── controllers/
│   │   └── suspense_meta_controller.py  # Iterative plot generation engine
│   ├── evaluation/
│   │   ├── reader_simulation.py     # Simulated reader evaluation
│   │   ├── feedback_aggregation.py  # Combine reader feedback
│   │   └── metrics.py              # Quality metrics
│   ├── data_structures/
│   │   └── facts.py                # Data classes for story elements
│   └── utils/
│       ├── config.py               # Configuration management
│       └── prompts.py              # LLM prompt templates
└── outputs/                    # Generated stories
```

## Setup

### Requirements

- Python 3.10+
- GPU with 6+ GB VRAM (for 4B model) or 16+ GB (for 8B model)

### Installation

```bash
git clone https://github.com/ivy3h/smokemirror.git
cd smokemirror
pip install torch transformers accelerate bitsandbytes pyyaml pydantic tqdm rich tabulate
```

## Usage

### Basic Usage

```bash
# Generate with default config (Qwen3-8B, 4-bit quantization)
python scripts/generate_story.py

# Specify crime type and setting
python scripts/generate_story.py --crime-type murder --setting "tech startup"

# Use a specific config
python scripts/generate_story.py --config configs/test_4b.yaml

# Test without GPU (mock mode)
python scripts/generate_story.py --mock
```

### Command Line Options

```bash
python scripts/generate_story.py \
  --config configs/test_4b.yaml \        # Config file path
  --model "Qwen/Qwen3-4B" \             # Override model
  --crime-type murder \                   # murder | embezzlement | art theft | corporate sabotage | kidnapping
  --setting "tech startup" \              # Story setting
  --num-conspirators 3 \                  # Number of conspirators (2-4)
  --min-plot-points 10 \                  # Minimum plot points
  --max-plot-points 20 \                  # Maximum plot points
  --output-dir "outputs" \               # Output directory
  --no-evaluation \                       # Skip reader evaluation
  --no-refinement \                       # Skip refinement loop
  --seed 42 \                             # Random seed
  --mock                                  # Use mock LLM (no GPU)
```

### Configuration Files

Configs are YAML files under `configs/`. Key sections:

```yaml
model:
  name: "Qwen/Qwen3-4B"       # Any HuggingFace causal LM
  load_in_4bit: false          # 4-bit quantization (saves VRAM)
  torch_dtype: "bfloat16"     # float16 | bfloat16 | float32
  max_new_tokens: 2048         # Max output tokens per LLM call
  temperature: 0.7             # Creativity (0.1=conservative, 1.0=creative)

generation:
  min_plot_points: 15          # Story length control
  max_plot_points: 25
  max_conspirators: 4          # Story complexity

suspense:
  collision_check_sensitivity: 0.5  # How often detective approaches truth

reader_simulation:
  enabled: false               # Set true for quality evaluation

refinement:
  max_iterations: 0            # 0 = skip refinement
```

Available configs:

| Config | Model | Quantization | VRAM | Use Case |
|--------|-------|-------------|------|----------|
| `test_4b.yaml` | Qwen3-4B | None | ~8 GB | Fast testing |
| `default.yaml` | Qwen3-8B | 4-bit | ~6 GB | Default |
| `test_qwen25_7b.yaml` | Qwen2.5-7B | None | ~14 GB | Alternative model |
| `test_32b.yaml` | Qwen3-32B | None | ~64 GB | High quality (multi-GPU) |

### Output

Each run produces files in `{output_dir}/`:

| File | Content |
|------|---------|
| `story_{run_id}.md` | Final narrative (Markdown) |
| `plot_points_{run_id}.json` | All plot points with metadata |
| `facts_{run_id}.json` | Real + fabricated crime facts |
| `metrics_{run_id}.json` | Quality metrics (if evaluation enabled) |

## Running on Google Colab

See [COLAB_GUIDE.md](COLAB_GUIDE.md) for detailed instructions. Quick start:

```python
# Cell 1 - Mount Drive & install
from google.colab import drive
drive.mount('/content/drive')

!pip install torch transformers accelerate bitsandbytes pyyaml pydantic tqdm rich tabulate
!git clone https://github.com/ivy3h/smokemirror.git
%cd smokemirror

# Cell 2 - Generate (results saved to Google Drive)
!mkdir -p "/content/drive/MyDrive/CS7634 AI Storytelling Project/results"

!python scripts/generate_story.py \
  --config configs/test_4b.yaml \
  --crime-type murder \
  --setting "tech startup" \
  --output-dir "/content/drive/MyDrive/CS7634 AI Storytelling Project/results"

# Cell 3 - Read the story
import glob
story_files = sorted(glob.glob("/content/drive/MyDrive/CS7634 AI Storytelling Project/results/story_*.md"))
if story_files:
    with open(story_files[-1]) as f:
        print(f.read())
```

Qwen3-4B runs on the free T4 GPU (16 GB). For more options (8B, 32B, custom parameters), see [COLAB_GUIDE.md](COLAB_GUIDE.md).

## Generation Pipeline

1. **Initialize LLM** — Load model from HuggingFace
2. **Generate Crime Backstory** — Real criminal, victims, conspirators, evidence, timeline
3. **Generate Fabricated Narrative** — False suspect, planted evidence, alibis
4. **Generate Detective Investigation** — Iterative plot points with suspense control
5. **Reader Evaluation** *(optional)* — Simulated readers assess quality
6. **Assemble Story** — Convert plot points to prose chapters

## License

This project is licensed under the [MIT License](LICENSE).
