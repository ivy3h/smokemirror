#!/bin/bash
#SBATCH -p overcap
#SBATCH --account=nlprx-lab
#SBATCH -t 6:00:00
#SBATCH --gres=gpu:a40:4
#SBATCH --cpus-per-task=16
#SBATCH --mem=200G
#SBATCH -J smokemirror_32b
#SBATCH -o /coc/pskynet6/jhe478/smokemirror/outputs/smokemirror_32b_%j.log

# Activate environment
source ~/.bashrc
conda activate tinker

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
pip install -q pyyaml pydantic tabulate rich tqdm accelerate

echo "=========================================="
echo "SMOKEMIRROR TEST - Qwen3-32B"
echo "=========================================="
echo "Model: Qwen/Qwen3-32B (Full Precision, Multi-GPU)"
echo "Thinking Mode: ENABLED"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'N/A')"
echo "Memory: $(nvidia-smi --query-gpu=memory.total --format=csv,noheader 2>/dev/null || echo 'N/A')"
echo "=========================================="

# Run the 32B test
python scripts/test_32b.py

echo ""
echo "=========================================="
echo "Test completed at $(date)"
echo "=========================================="
