#!/bin/bash
#SBATCH -p overcap
#SBATCH --account=nlprx-lab
#SBATCH -t 8:00:00
#SBATCH --gres=gpu:a40:4
#SBATCH --cpus-per-task=16
#SBATCH --mem=200G
#SBATCH -J smokemirror_dual_detective
#SBATCH -o /coc/pskynet6/jhe478/smokemirror/outputs/dual_detective_%j.log

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

# Install dependencies
pip install -q pyyaml pydantic tabulate rich tqdm accelerate

echo "=========================================="
echo "SMOKEMIRROR - DUAL DETECTIVE MODE"
echo "=========================================="
echo "Model: Qwen/Qwen3-32B (Full Precision)"
echo "Mode: TWO DETECTIVES (One Real, One Killer)"
echo "Premise: Killer-detective misleads real detective"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'N/A')"
echo "=========================================="

# Run dual detective generation
python scripts/generate_dual_detective.py

echo ""
echo "=========================================="
echo "Generation completed at $(date)"
echo "=========================================="
