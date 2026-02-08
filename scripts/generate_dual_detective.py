#!/usr/bin/env python3
"""
Dual Detective story generation script.
One detective is real, one is the killer in disguise.
The killer-detective misleads the real detective throughout the investigation.

LLM freely plans the chapter structure while ensuring key mystery elements.
"""

import os
import sys
import json
import re
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


def generate_dual_detective_story(llm) -> str:
    """Generate a mystery novel with two detectives - one real, one killer."""

    sections = []

    # Step 1: Generate complete story concept with all mystery elements
    logger.info("\n[1/4] Generating story concept and mystery elements...")

    concept_prompt = """You are an award-winning mystery novelist. Create a complete crime mystery novel blueprint.

## THE CORE PREMISE:

Two detectives are assigned to investigate a murder case together. What no one knows - except the reader - is that ONE OF THE DETECTIVES IS THE KILLER.

## REQUIRED MYSTERY ELEMENTS:

### 1. THE CRIME (犯罪过程)
- What happened, how, when, where
- The killer-detective's motive and method
- How they planned and executed the murder
- What evidence was left behind

### 2. THE CHARACTERS
- **Detective A (Real Detective)**: Skilled investigator, trusts their partner
- **Detective B (Killer-Detective)**: Committed the murder, now investigating their own crime
- **The Victim**: Who they were, why they were killed
- **Suspects (4-7 people)**: Each with relationship to victim, motive, and opportunity

### 3. ALIBIS (不在场证明)
For each suspect, create:
- Their claimed alibi for the time of murder
- Whether the alibi is solid, weak, or false
- Who can verify (or contradict) their alibi
- Detective B's fake alibi and how they maintain it

### 4. RED HERRINGS (误导线索/红鲱鱼)
Create 3-5 misleading clues that:
- Point toward innocent suspects
- Are planted or highlighted by Detective B
- Seem convincing but have innocent explanations
- Distract from the real evidence

### 5. KEY CLUES (关键线索)
Create 4-6 crucial pieces of evidence that:
- Could expose Detective B if properly analyzed
- Are overlooked, misinterpreted, or hidden
- Eventually lead Detective A to the truth
- Include physical evidence, witness statements, and behavioral inconsistencies

### 6. THE INVESTIGATION PROCESS (破案过程)
- How the case unfolds step by step
- Key interviews and discoveries
- Moments where Detective A gets close to the truth
- How Detective B deflects and misdirects

## OUTPUT FORMAT:

```
# [Your Creative Novel Title]

*A Mystery Novel*

---

## Prologue: [Title]

[800-1200 words showing the murder from Detective B's perspective, their motive, and decision to join the investigation]

---

## Story Blueprint

### The Crime
**Date/Time**: [When]
**Location**: [Where]
**Method**: [How the victim was killed]
**Motive**: [Why Detective B committed the murder]

### The Victim
**Name**: [Full name]
**Background**: [Who they were]
**Connection to Killer**: [Why Detective B wanted them dead]

### The Detectives
**Detective A (Real)**: [Name] - [Personality, skills, weaknesses]
**Detective B (Killer)**: [Name] - [Public persona vs true nature]

### The Suspects

**Suspect 1**: [Name]
- Relationship to victim: [...]
- Apparent motive: [...]
- Alibi: [Their claimed whereabouts]
- Alibi strength: [Solid/Weak/False]
- Why they seem guilty: [...]

**Suspect 2**: [Name]
[Same format...]

[Continue for 4-7 suspects total]

### Red Herrings (误导线索)

1. **[Red Herring 1]**: [Description] - Points to: [Which suspect] - True explanation: [Why it's misleading]
2. **[Red Herring 2]**: [...]
3. **[Red Herring 3]**: [...]
[Add more as needed]

### Key Clues (关键线索)

1. **[Clue 1]**: [Description] - Significance: [What it really means] - Status: [Found/Hidden/Misinterpreted]
2. **[Clue 2]**: [...]
3. **[Clue 3]**: [...]
[Add more as needed]

### Detective B's Cover
- **Fake Alibi**: [How they explain their whereabouts]
- **Evidence Tampering**: [What they've hidden or altered]
- **Misdirection Tactics**: [How they guide A toward wrong suspects]
```

Create this complete blueprint now:"""

    response = llm.generate(
        prompt=concept_prompt,
        max_new_tokens=6000,
        temperature=0.9,
    )

    concept_text = llm._strip_thinking_tags(response.text)
    sections.append(concept_text)

    # Step 2: Generate chapter outline (LLM decides structure)
    logger.info("\n[2/4] Generating chapter outline (LLM decides structure)...")

    outline_prompt = f"""Based on the story blueprint below, create a detailed chapter outline.

## STORY BLUEPRINT:
{concept_text[:8000]}

## YOUR TASK:

Design the chapter structure for this mystery novel. YOU decide:
- How many chapters (typically 8-15 for a mystery novel)
- What happens in each chapter
- The pacing and progression

## REQUIREMENTS:

Each chapter outline must specify:
1. **Chapter title**
2. **Main events** (what happens)
3. **Investigation progress** (what clues are found/missed)
4. **Character dynamics** (A and B's relationship)
5. **Suspense elements** (near-discoveries, tension)

## MUST INCLUDE across the chapters:

- [ ] The crime scene investigation
- [ ] Interviewing all suspects
- [ ] Checking alibis (some verified, some broken)
- [ ] Discovery of red herrings (misleading A)
- [ ] Discovery of key clues (some overlooked)
- [ ] Detective B's misdirection moments
- [ ] Close calls where B almost gets caught
- [ ] A's growing suspicion
- [ ] A's secret investigation of B
- [ ] The truth revealed
- [ ] Confrontation between A and B
- [ ] Resolution

## OUTPUT FORMAT:

```
## Chapter Outline

**Total Chapters**: [Number]

### Chapter 1: [Title]
- **Focus**: [Main theme]
- **Events**: [What happens]
- **Clues**: [Evidence found/missed]
- **A & B Dynamic**: [Their interaction]
- **Suspense**: [Tension elements]

### Chapter 2: [Title]
[Same format...]

[Continue for all chapters...]

### Epilogue: [Title]
- **Focus**: [Aftermath]
- **Resolution**: [How it ends]
```

Create the chapter outline now:"""

    outline_response = llm.generate(
        prompt=outline_prompt,
        max_new_tokens=4000,
        temperature=0.8,
    )

    outline_text = llm._strip_thinking_tags(outline_response.text)
    sections.append("\n\n---\n\n" + outline_text)

    # Parse the outline to get chapter count
    chapter_matches = re.findall(r'###\s*Chapter\s*(\d+)', outline_text)
    if chapter_matches:
        num_chapters = max(int(c) for c in chapter_matches)
    else:
        num_chapters = 10  # fallback

    logger.info(f"LLM planned {num_chapters} chapters")

    # Step 3: Generate each chapter
    logger.info(f"\n[3/4] Generating {num_chapters} chapters...")

    for chapter_num in range(1, num_chapters + 1):
        logger.info(f"  Writing Chapter {chapter_num}/{num_chapters}...")

        # Extract this chapter's outline
        chapter_pattern = rf'###\s*Chapter\s*{chapter_num}[:\s]*(.*?)(?=###\s*Chapter\s*\d+|###\s*Epilogue|$)'
        chapter_outline_match = re.search(chapter_pattern, outline_text, re.DOTALL | re.IGNORECASE)
        chapter_outline = chapter_outline_match.group(0) if chapter_outline_match else f"Chapter {chapter_num}"

        chapter_prompt = f"""Write Chapter {chapter_num} of this mystery novel.

## STORY BLUEPRINT (reference):
{concept_text[:4000]}...

## CHAPTER OUTLINE:
{chapter_outline}

## WRITING REQUIREMENTS:

1. **LENGTH**: 1500-2500 words of polished literary prose

2. **DUAL PERSPECTIVE**:
   - Show Detective A's perspective (trusting, investigating)
   - Reveal Detective B's true thoughts to the reader
   - Use dramatic irony: reader knows B is the killer

3. **MYSTERY ELEMENTS**:
   - Reference alibis, clues, and suspects from the blueprint
   - Show the investigation process realistically
   - Include interview scenes, evidence examination
   - B's subtle misdirections should be visible to the reader

4. **DIALOGUE**: Natural, with B's words having double meanings

5. **ATMOSPHERE**: Tension, suspense, psychological depth

6. **FORMAT**:

## Chapter {chapter_num}: [Creative Title]

[Chapter content...]

---

Write Chapter {chapter_num} now:"""

        chapter_response = llm.generate(
            prompt=chapter_prompt,
            max_new_tokens=6000,
            temperature=0.8,
        )

        chapter_text = llm._strip_thinking_tags(chapter_response.text)
        sections.append("\n\n" + chapter_text)

    # Step 4: Generate epilogue
    logger.info("\n[4/4] Generating epilogue...")

    epilogue_prompt = f"""Write the epilogue for this mystery novel.

## STORY CONTEXT:
{concept_text[:2000]}...

## EPILOGUE REQUIREMENTS (800-1200 words):

1. **AFTERMATH**:
   - Detective B's fate (arrest, trial, confession)
   - Innocent suspects cleared
   - Victim's family finding closure

2. **DETECTIVE A'S RECKONING**:
   - Processing the betrayal
   - Reflecting on missed signs
   - How this changes them

3. **FINAL IMAGE**:
   - A powerful closing scene
   - Resolution with lingering weight

## FORMAT:

## Epilogue: [Title]

[Epilogue content...]

Write the epilogue now:"""

    epilogue_response = llm.generate(
        prompt=epilogue_prompt,
        max_new_tokens=4096,
        temperature=0.8,
    )

    epilogue_text = llm._strip_thinking_tags(epilogue_response.text)
    sections.append("\n\n" + epilogue_text)

    return "\n".join(sections)


def main():
    """Generate a dual-detective mystery novel."""
    logger.info("=" * 60)
    logger.info("SMOKEMIRROR - DUAL DETECTIVE MODE (Free Structure)")
    logger.info("=" * 60)
    logger.info("One detective is real. One is the killer.")
    logger.info("LLM freely plans chapter structure with required elements.")
    logger.info("=" * 60)

    from src.utils.config import load_config
    from src.models.llm_wrapper import create_llm_wrapper

    # Load 32B config
    config = load_config(str(project_root / "configs" / "test_32b.yaml"))
    config.set_seed()

    logger.info(f"Model: {config.model.name}")
    logger.info("Mode: DUAL DETECTIVE (free chapter planning)")

    # Initialize LLM
    logger.info("\nLoading model...")
    llm = create_llm_wrapper(config.model, use_mock=False)

    # Generate story
    logger.info("\n" + "=" * 60)
    logger.info("GENERATING STORY...")
    logger.info("=" * 60)

    story = generate_dual_detective_story(llm)

    # Save output
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = project_root / "outputs" / f"dual_detective_{run_id}"
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
