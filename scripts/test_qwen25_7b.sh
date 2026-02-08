#!/bin/bash
#SBATCH -p overcap
#SBATCH --account=nlprx-lab
#SBATCH -t 3:00:00
#SBATCH --gres=gpu:a40:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=48G
#SBATCH -J smokemirror_qwen25
#SBATCH -o /coc/pskynet6/jhe478/smokemirror/outputs/smokemirror_qwen25_7b_%j.log

# Activate environment
source ~/.bashrc
conda activate base

# Set HuggingFace cache to coc6 storage
export HF_HOME=/coc/pskynet6/jhe478/huggingface
export TRANSFORMERS_CACHE=/coc/pskynet6/jhe478/huggingface
export HF_DATASETS_CACHE=/coc/pskynet6/jhe478/huggingface/datasets
export TOKENIZERS_PARALLELISM=false

# Set working directory
cd /coc/pskynet6/jhe478/smokemirror

# Create outputs directory
mkdir -p outputs

# Install dependencies if needed
pip install -q pyyaml pydantic tabulate rich tqdm accelerate bitsandbytes

echo "=========================================="
echo "SMOKEMIRROR - Qwen2.5-7B-Instruct"
echo "Config: configs/test_qwen25_7b.yaml"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'N/A')"
echo "Memory: $(nvidia-smi --query-gpu=memory.total --format=csv,noheader 2>/dev/null || echo 'N/A')"
echo "=========================================="

# Run full story generation pipeline
python scripts/generate_story.py \
    --config configs/test_qwen25_7b.yaml \
    --crime-type murder \
    --setting "tech startup" \
    --output-dir outputs \
    --seed 42

echo ""
echo "=========================================="
echo "Generation completed at $(date)"
echo "=========================================="
