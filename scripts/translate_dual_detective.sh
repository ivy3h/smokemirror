#!/bin/bash
#SBATCH -p overcap
#SBATCH --account=nlprx-lab
#SBATCH -t 2:00:00
#SBATCH --gres=gpu:a40:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=50G
#SBATCH -J translate_story
#SBATCH -o /coc/pskynet6/jhe478/smokemirror/outputs/translate_%j.log

source ~/.bashrc
conda activate tinker

export HF_HOME=/coc/pskynet6/jhe478/huggingface
export TRANSFORMERS_CACHE=/coc/pskynet6/jhe478/huggingface

cd /coc/pskynet6/jhe478/smokemirror

echo "=========================================="
echo "STORY TRANSLATION - English to Chinese"
echo "=========================================="

python scripts/translate_story.py \
    --input /coc/pskynet6/jhe478/smokemirror/outputs/dual_detective_20260207_201039/story.md \
    --output /coc/pskynet6/jhe478/smokemirror/outputs/dual_detective_20260207_201039/story_chinese.md \
    --model Qwen/Qwen2.5-7B-Instruct

echo ""
echo "Translation completed at $(date)"
