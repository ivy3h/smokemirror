#!/bin/bash
#SBATCH -p overcap
#SBATCH --account=nlprx-lab
#SBATCH -t 4:00:00
#SBATCH --gres=gpu:a40:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH -J smokemirror_readers
#SBATCH -o /coc/pskynet6/jhe478/smokemirror/outputs/smokemirror_readers_%j.log

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
pip install -q pyyaml pydantic tabulate rich tqdm

echo "=========================================="
echo "SMOKEMIRROR TEST WITH READER SIMULATION"
echo "=========================================="
echo "Story Model: Qwen/Qwen3-4B"
echo "Reader Models:"
echo "  - Qwen/Qwen2.5-7B-Instruct"
echo "  - deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'N/A')"
echo "Memory: $(nvidia-smi --query-gpu=memory.total --format=csv,noheader 2>/dev/null || echo 'N/A')"
echo "=========================================="

# Run the test with readers
python scripts/test_with_readers.py

echo ""
echo "=========================================="
echo "Test completed at $(date)"
echo "=========================================="
