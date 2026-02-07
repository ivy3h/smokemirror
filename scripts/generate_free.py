#!/usr/bin/env python3
"""
Free-form story generation script.
Gives the model maximum creative freedom within structural requirements.
"""

import os
import sys
import json
import logging
from datetime import datetime

# Set HuggingFace cache before imports
os.environ["HF_HOME"] = "/coc/pskynet6/jhe478/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/coc/pskynet6/jhe478/huggingface"

from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def generate_story_free(llm, num_chapters: int = 8) -> str:
    """Generate a complete mystery novel with maximum creative freedom."""

    sections = []

    # Step 1: Generate the complete story concept, title, and prologue
    logger.info("\n[1/3] Generating story concept, title, and prologue...")

    concept_prompt = """你是一位屡获殊荣的悬疑小说作家。请创作一部完整的犯罪悬疑小说。

## 核心创作要求（必须遵循）：

1. **群体阴谋结构**：
   - 一个主要罪犯 + 2-4名共谋者
   - 他们共同犯下了一桩严重罪行（谋杀、诈骗、盗窃等）
   - 他们精心策划了一个虚假叙事来掩盖真相
   - 他们将嫌疑引向一个无辜的替罪羊

2. **双重叙事结构**：
   - 读者从一开始就知道真相（谁是真正的罪犯，动机是什么）
   - 侦探在虚假叙事中调查，不知道真相
   - 故事同时展现两个层面：读者看到的真相 vs 侦探看到的假象

3. **悬念机制**：
   - 读者知道的永远比侦探多
   - 读者眼睁睁看着侦探一步步走入陷阱
   - 共谋者会在关键时刻介入，破坏侦探接近真相的机会
   - 每当侦探快要发现真相时，就会被误导到错误的方向

4. **结局**：
   - 阴谋几乎成功，但在最后关头出现转折
   - 侦探通过某个意外发现（被忽略的细节、共谋者的失误、良心发现的告密者）揭开真相
   - 双重叙事在结尾合二为一：读者和侦探终于站在同一视角
   - 真相大白，正义得以伸张（或部分伸张）

## 你的任务：

请创作：
1. **小说标题**：一个富有文学性、引人入胜的标题
2. **序章（800-1200字）**：
   - 设定时间、地点、氛围
   - 向读者（而非侦探）揭示罪行的真相
   - 介绍罪犯、共谋者、受害者、替罪羊
   - 展示他们的阴谋计划
   - 以悬念结尾，引出侦探的登场

## 格式要求：

```
# [你创作的小说标题]

*一部悬疑小说*

---

## 序章：[序章标题]

[序章正文...]

---

## 故事设定（供后续章节使用）

**罪行**：[具体描述]
**真正的罪犯**：[姓名] - [职业/身份] - [动机]
**共谋者**：
- [姓名1] - [职业] - [在阴谋中的角色]
- [姓名2] - [职业] - [在阴谋中的角色]
- [姓名3] - [职业] - [在阴谋中的角色]（如果有）
**受害者**：[姓名] - [职业/身份]
**替罪羊**：[姓名] - [为什么会被陷害]
**阴谋计划**：[他们如何掩盖真相、误导调查]
**侦探**：[姓名] - [简要描述]
```

现在开始创作："""

    response = llm.generate(
        prompt=concept_prompt,
        max_new_tokens=4096,
        temperature=0.9,
    )

    concept_text = llm._strip_thinking_tags(response.text)
    sections.append(concept_text)

    # Extract story settings for chapter generation
    logger.info("Parsing story settings...")

    # Step 2: Generate chapters
    logger.info(f"\n[2/3] Generating {num_chapters} chapters...")

    for chapter_num in range(1, num_chapters + 1):
        logger.info(f"  Writing Chapter {chapter_num}/{num_chapters}...")

        # Determine chapter focus based on position
        if chapter_num == 1:
            chapter_focus = "侦探首次介入调查，发现初步线索，但这些线索都指向错误的方向"
        elif chapter_num == 2:
            chapter_focus = "侦探深入调查，共谋者开始暗中破坏，误导性证据出现"
        elif chapter_num <= num_chapters // 2:
            chapter_focus = "调查陷入僵局或被误导，侦探越来越相信虚假叙事"
        elif chapter_num == num_chapters // 2 + 1:
            chapter_focus = "侦探几乎接近真相的危险时刻，共谋者紧急介入化解危机"
        elif chapter_num < num_chapters - 1:
            chapter_focus = "侦探完全被误导，证据链条指向替罪羊"
        elif chapter_num == num_chapters - 1:
            chapter_focus = "关键转折：侦探发现一个被忽略的细节，或共谋者犯下致命失误，或有人良心发现。侦探开始怀疑之前的结论"
        else:
            chapter_focus = "真相大白：侦探揭开整个阴谋，双重叙事合二为一。读者和侦探终于站在同一视角，正义得以伸张"

        chapter_prompt = f"""继续创作这部悬疑小说的第 {chapter_num} 章。

## 前文概要：
{concept_text[:3000]}...

## 本章重点：
{chapter_focus}

## 写作要求：

1. **长度**：1500-2500字的精雕细琢的文学散文

2. **场景描写**：
   - 开篇用生动的氛围描写（天气、光线、声音、气味）
   - 让读者沉浸在具体的时间和地点中

3. **对话**：
   - 包含3-5段实质性的对话交流
   - 通过对话展现人物性格、隐藏的秘密、微妙的谎言
   - 共谋者的对话要有弦外之音（读者能察觉，侦探察觉不到）

4. **双重视角**：
   - 展示侦探的推理过程（他/她看到了什么、推断了什么）
   - 同时让读者看到真相（共谋者在暗中做什么）
   - 制造戏剧性反讽：读者知道侦探错了，却只能眼睁睁看着

5. **悬念构建**：
   - 每当侦探接近真相，就有意外让他/她转向错误方向
   - 共谋者的介入要自然、不露痕迹
   - 让读者感到紧张和无奈

6. **人物塑造**：
   - 给每个出场人物独特的小动作、说话方式
   - 侦探要有血有肉，让读者同情他/她的困境
   - 共谋者要表演得天衣无缝

7. **纯粹的叙事散文**：
   - 不要元评论
   - 不要"情节点1"之类的标注
   - 像出版的文学惊悚小说一样写作

## 格式：

## 第{chapter_num}章：[你创作的章节标题]

[章节正文...]

---

现在创作第 {chapter_num} 章："""

        chapter_response = llm.generate(
            prompt=chapter_prompt,
            max_new_tokens=6000,
            temperature=0.8,
        )

        chapter_text = llm._strip_thinking_tags(chapter_response.text)
        sections.append("\n\n" + chapter_text)

    # Step 3: Generate epilogue
    logger.info("\n[3/3] Generating epilogue...")

    epilogue_prompt = f"""为这部悬疑小说写一个令人难忘的尾声。

## 故事概要：
{concept_text[:2000]}...

## 尾声要求（800-1200字）：

1. **时间跳跃**：从真相大白后数周或数月开始

2. **正义的代价**：
   - 真正的罪犯和共谋者的结局——法律制裁、社会唾弃、或内心的煎熬
   - 有人认罪伏法，有人仍在逃避，有人选择了极端的方式
   - 展示他们各自的"之后"——铁窗生涯、流亡海外、或彻底崩溃

3. **受害者与幸存者**：
   - 曾被冤枉的替罪羊如何重建生活
   - 受害者家属的释然或仍未平复的创伤
   - 那些无辜卷入的人如何继续前行

4. **侦探的反思**：
   - 侦探回顾整个案件——那些差点被蒙蔽的时刻
   - 是什么让他/她最终看穿了真相？
   - 对这个案件的体悟，对人性阴暗面的理解

5. **结尾意象**：
   - 以一个强有力的意象收尾
   - 暗示正义虽迟但到，或真相的重量永远不会消散
   - 让读者感到释然中带着沉重

4. **语调**：
   - 文学性的、沉思的、带有释然
   - 像风暴过后的宁静，阳光穿透乌云
   - 余韵悠长，但这次是希望的余韵

## 格式：

## 尾声

[尾声正文...]

现在创作尾声："""

    epilogue_response = llm.generate(
        prompt=epilogue_prompt,
        max_new_tokens=4096,
        temperature=0.8,
    )

    epilogue_text = llm._strip_thinking_tags(epilogue_response.text)
    sections.append("\n\n" + epilogue_text)

    return "\n".join(sections)


def main():
    """Generate a free-form mystery novel."""
    logger.info("=" * 60)
    logger.info("SMOKEMIRROR - FREE CREATION MODE")
    logger.info("=" * 60)

    from src.utils.config import load_config
    from src.models.llm_wrapper import create_llm_wrapper

    # Load 32B config
    config = load_config(str(project_root / "configs" / "test_32b.yaml"))
    config.set_seed()

    logger.info(f"Model: {config.model.name}")
    logger.info("Mode: FREE CREATION (model creates everything)")
    logger.info("Requirements: Conspiracy, Dual Narrative, Reader-knows-more Suspense")

    # Initialize LLM
    logger.info("\nLoading model...")
    llm = create_llm_wrapper(config.model, use_mock=False)

    # Generate story
    logger.info("\n" + "=" * 60)
    logger.info("GENERATING STORY...")
    logger.info("=" * 60)

    story = generate_story_free(llm, num_chapters=8)

    # Save output
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = project_root / "outputs" / f"free_story_{run_id}"
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "story.md", "w", encoding="utf-8") as f:
        f.write(story)

    # Count words
    word_count = len(story.split())
    char_count = len(story)

    logger.info("\n" + "=" * 60)
    logger.info("GENERATION COMPLETED!")
    logger.info("=" * 60)
    logger.info(f"Output: {output_dir / 'story.md'}")
    logger.info(f"Length: ~{word_count} words, {char_count} characters")

    # Preview
    print("\n" + "=" * 60)
    print("STORY PREVIEW (first 3000 chars)")
    print("=" * 60)
    print(story[:3000])
    if len(story) > 3000:
        print("\n... [truncated] ...")

    return 0


if __name__ == "__main__":
    sys.exit(main())
