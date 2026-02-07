#!/usr/bin/env python3
"""
Translate a generated story from English to Chinese using LLM.
"""

import os
import sys
import re
import logging
import argparse
from datetime import datetime

# Set HuggingFace cache before imports
os.environ["HF_HOME"] = "/coc/pskynet6/jhe478/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/coc/pskynet6/jhe478/huggingface"

from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def translate_chunk(llm, text: str, context: str = "") -> str:
    """Translate a chunk of text to Chinese."""

    prompt = f"""你是一位专业的文学翻译家，擅长将英文悬疑小说翻译成流畅优美的中文。

请将以下英文小说片段翻译成中文。要求：
1. 保持原文的文学风格和悬疑氛围
2. 人名保留英文原名
3. 使用自然流畅的中文表达
4. 保留原文的段落结构
5. 对话用中文引号「」
6. 保持原文的戏剧张力和节奏感

{f"上下文提示：{context}" if context else ""}

需要翻译的内容：

{text}

翻译结果（直接输出中文译文，不要任何解释）："""

    response = llm.generate(
        prompt=prompt,
        max_new_tokens=4096,
        temperature=0.3,  # Lower temperature for more consistent translation
        disable_thinking=True,
    )

    return response.text.strip()


def split_into_sections(story: str) -> list[tuple[str, str]]:
    """Split story into sections (chapters, prologue, epilogue)."""

    sections = []

    # Split by ## headers
    parts = re.split(r'(## [^\n]+)', story)

    current_title = "Opening"
    current_content = ""

    for part in parts:
        if part.startswith('## '):
            if current_content.strip():
                sections.append((current_title, current_content.strip()))
            current_title = part.strip()
            current_content = ""
        else:
            current_content += part

    # Don't forget the last section
    if current_content.strip():
        sections.append((current_title, current_content.strip()))

    return sections


def main():
    parser = argparse.ArgumentParser(description='Translate story to Chinese')
    parser.add_argument('input_file', help='Path to the story.md file')
    parser.add_argument('--model', default='Qwen/Qwen2.5-7B-Instruct', help='Model to use for translation')
    parser.add_argument('--output', help='Output file path (default: story_chinese.md in same directory)')
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        return 1

    output_path = Path(args.output) if args.output else input_path.parent / "story_chinese.md"

    logger.info("=" * 60)
    logger.info("STORY TRANSLATION - English to Chinese")
    logger.info("=" * 60)
    logger.info(f"Input: {input_path}")
    logger.info(f"Output: {output_path}")
    logger.info(f"Model: {args.model}")

    # Load story
    with open(input_path, 'r', encoding='utf-8') as f:
        story = f.read()

    logger.info(f"Story length: {len(story)} characters, ~{len(story.split())} words")

    # Initialize LLM
    from src.models.llm_wrapper import LLMWrapper
    from src.utils.config import ModelConfig

    model_config = ModelConfig(
        name=args.model,
        device="auto",
        load_in_4bit=False,
        load_in_8bit=False,
        torch_dtype="bfloat16",
        max_new_tokens=4096,
        temperature=0.3,
        top_p=0.9,
        do_sample=True,
    )

    logger.info("\nLoading translation model...")
    llm = LLMWrapper(model_config)

    # Split into sections
    sections = split_into_sections(story)
    logger.info(f"Found {len(sections)} sections to translate")

    # Translate each section
    translated_sections = []

    # Translate title and opening
    translated_sections.append("# 双重叙事\n\n")
    translated_sections.append("*一部犯罪悬疑小说*\n\n")
    translated_sections.append("---\n\n")

    for i, (title, content) in enumerate(sections):
        # Skip the title section (we added our own)
        if title == "Opening" and "# The Dual Narrative" in content:
            continue

        logger.info(f"\n[{i+1}/{len(sections)}] Translating: {title}")

        # Translate title
        if title.startswith("## "):
            title_text = title[3:]
            if "Prologue" in title_text:
                translated_title = "## 序章：烟幕背后的真相"
            elif "Epilogue" in title_text:
                translated_title = "## 尾声"
            elif "Chapter" in title_text:
                # Extract chapter number and title
                match = re.match(r'Chapter (\d+): (.+)', title_text)
                if match:
                    chapter_num = match.group(1)
                    chapter_title = match.group(2)
                    # Translate chapter title
                    title_prompt = f"将以下章节标题翻译成中文（只输出翻译结果）：{chapter_title}"
                    translated_chapter_title = llm.generate(
                        prompt=title_prompt,
                        max_new_tokens=100,
                        temperature=0.3,
                        disable_thinking=True,
                    ).text.strip()
                    translated_title = f"## 第{chapter_num}章：{translated_chapter_title}"
                else:
                    translated_title = title
            else:
                translated_title = title
        else:
            translated_title = title

        # Translate content in chunks if too long
        if len(content) > 3000:
            # Split by paragraphs
            paragraphs = content.split('\n\n')
            chunks = []
            current_chunk = []
            current_length = 0

            for para in paragraphs:
                if current_length + len(para) > 2500 and current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                    current_chunk = [para]
                    current_length = len(para)
                else:
                    current_chunk.append(para)
                    current_length += len(para)

            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))

            translated_content_parts = []
            for j, chunk in enumerate(chunks):
                logger.info(f"  Translating chunk {j+1}/{len(chunks)}...")
                translated_chunk = translate_chunk(llm, chunk, f"这是{translated_title}的一部分")
                translated_content_parts.append(translated_chunk)

            translated_content = '\n\n'.join(translated_content_parts)
        else:
            translated_content = translate_chunk(llm, content, f"这是{translated_title}")

        translated_sections.append(f"{translated_title}\n\n")
        translated_sections.append(f"{translated_content}\n\n")
        translated_sections.append("---\n\n")

    # Combine and save
    translated_story = ''.join(translated_sections)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(translated_story)

    logger.info("\n" + "=" * 60)
    logger.info("TRANSLATION COMPLETED!")
    logger.info("=" * 60)
    logger.info(f"Output saved to: {output_path}")
    logger.info(f"Translated length: {len(translated_story)} characters")

    return 0


if __name__ == "__main__":
    sys.exit(main())
