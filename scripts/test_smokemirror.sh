#!/bin/bash
#SBATCH -p overcap
#SBATCH --account=nlprx-lab
#SBATCH -t 2:00:00
#SBATCH --gres=gpu:a40:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32G
#SBATCH -J smokemirror_test
#SBATCH -o /nethome/jhe478/smokemirror/outputs/smokemirror_test_%j.log

# Activate environment
source ~/.bashrc
conda activate tinker

# Set HuggingFace cache to coc6 storage
export HF_HOME=/coc/pskynet6/jhe478/huggingface
export TRANSFORMERS_CACHE=/coc/pskynet6/jhe478/huggingface
export HF_DATASETS_CACHE=/coc/pskynet6/jhe478/huggingface/datasets
export TOKENIZERS_PARALLELISM=false

# Set working directory
cd /nethome/jhe478/smokemirror

# Create outputs directory
mkdir -p outputs

# Install dependencies if needed
pip install -q pyyaml pydantic tabulate rich tqdm

echo "=========================================="
echo "SMOKEMIRROR TEST"
echo "Model: Qwen/Qwen3-0.6B"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'N/A')"
echo "=========================================="

# Run the simple test first
python scripts/test_simple.py

echo ""
echo "=========================================="
echo "Test completed at $(date)"
echo "=========================================="
