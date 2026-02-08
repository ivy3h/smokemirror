#!/bin/bash
#SBATCH -p overcap
#SBATCH --account=nlprx-lab
#SBATCH -t 3:00:00
#SBATCH --gres=gpu:a40:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH -J translate_story
#SBATCH -o /coc/pskynet6/jhe478/smokemirror/outputs/translate_%j.log

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

echo "=========================================="
echo "STORY TRANSLATION - English to Chinese"
echo "=========================================="
echo "Model: Qwen/Qwen2.5-7B-Instruct"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'N/A')"
echo "=========================================="

# Translate the story
python scripts/translate_story.py --input "$1" --model "Qwen/Qwen2.5-7B-Instruct"

echo ""
echo "=========================================="
echo "Translation completed at $(date)"
echo "=========================================="
