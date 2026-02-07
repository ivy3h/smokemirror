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

    concept_prompt = """You are an award-winning mystery novelist. Create a complete crime mystery novel.

## CORE STRUCTURAL REQUIREMENTS (Must Follow):

1. **CONSPIRACY STRUCTURE**:
   - One main criminal + 2-4 conspirators
   - They have committed a serious crime together (murder, fraud, theft, etc.)
   - They have carefully constructed a false narrative to cover up the truth
   - They have framed an innocent person as the scapegoat

2. **DUAL NARRATIVE STRUCTURE**:
   - The READER knows the truth from the beginning (who the real criminal is, what the motive was)
   - The DETECTIVE investigates within the false narrative, unaware of the truth
   - The story simultaneously shows both layers: the truth the reader sees vs. the illusion the detective sees

3. **SUSPENSE MECHANISM**:
   - The reader always knows more than the detective
   - The reader watches helplessly as the detective walks step by step into the trap
   - Conspirators intervene at critical moments to prevent the detective from getting close to the truth
   - Whenever the detective is about to discover the truth, they are misled in the wrong direction

4. **ENDING**:
   - The conspiracy almost succeeds, but at the last moment there is a turning point
   - The detective uncovers the truth through an unexpected discovery (an overlooked detail, a conspirator's mistake, a whistleblower with a guilty conscience)
   - The dual narratives merge at the end: the reader and the detective finally share the same perspective
   - The truth is revealed, justice is served (or partially served)

## YOUR TASK:

Create:
1. **NOVEL TITLE**: A literary, evocative, memorable title
2. **PROLOGUE (800-1200 words)**:
   - Establish the time, place, and atmosphere
   - Reveal the truth of the crime to the reader (but not the detective)
   - Introduce the criminal, conspirators, victim, and scapegoat
   - Show their conspiracy plan
   - End with a hook that leads to the detective's entrance

## FORMAT REQUIREMENTS:

```
# [Your Creative Novel Title]

*A Mystery Novel*

---

## Prologue: [Prologue Title]

[Prologue text...]

---

## Story Settings (for subsequent chapters)

**The Crime**: [Specific description]
**The Real Criminal**: [Name] - [Occupation/Identity] - [Motive]
**Conspirators**:
- [Name1] - [Occupation] - [Role in the conspiracy]
- [Name2] - [Occupation] - [Role in the conspiracy]
- [Name3] - [Occupation] - [Role in the conspiracy] (if applicable)
**The Victim**: [Name] - [Occupation/Identity]
**The Scapegoat**: [Name] - [Why they are being framed]
**The Conspiracy Plan**: [How they cover up the truth and mislead the investigation]
**The Detective**: [Name] - [Brief description]
```

Begin creating now:"""

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
            chapter_focus = "The detective first enters the investigation, discovers preliminary clues, but these clues all point in the wrong direction"
        elif chapter_num == 2:
            chapter_focus = "The detective digs deeper, conspirators begin their covert sabotage, misleading evidence appears"
        elif chapter_num <= num_chapters // 2:
            chapter_focus = "The investigation hits a dead end or is misdirected, the detective increasingly believes the false narrative"
        elif chapter_num == num_chapters // 2 + 1:
            chapter_focus = "A dangerous moment when the detective almost approaches the truth, conspirators urgently intervene to defuse the crisis"
        elif chapter_num < num_chapters - 1:
            chapter_focus = "The detective is completely misled, the chain of evidence points to the scapegoat"
        elif chapter_num == num_chapters - 1:
            chapter_focus = "KEY TURNING POINT: The detective discovers an overlooked detail, or a conspirator makes a fatal mistake, or someone's conscience awakens. The detective begins to doubt their previous conclusions"
        else:
            chapter_focus = "THE TRUTH REVEALED: The detective uncovers the entire conspiracy, the dual narratives merge into one. The reader and the detective finally share the same perspective, justice is served"

        chapter_prompt = f"""Continue writing Chapter {chapter_num} of this mystery novel.

## STORY SUMMARY SO FAR:
{concept_text[:3000]}...

## THIS CHAPTER'S FOCUS:
{chapter_focus}

## WRITING REQUIREMENTS:

1. **LENGTH**: 1500-2500 words of polished literary prose

2. **SCENE-SETTING**:
   - Open with vivid atmospheric description (weather, lighting, sounds, smells)
   - Immerse the reader in a specific time and place

3. **DIALOGUE**:
   - Include 3-5 substantial dialogue exchanges
   - Through dialogue, reveal character personalities, hidden secrets, subtle lies
   - Conspirators' dialogue should have subtext (the reader can detect it, the detective cannot)

4. **DUAL PERSPECTIVE**:
   - Show the detective's reasoning process (what they see, what they deduce)
   - Simultaneously let the reader see the truth (what the conspirators are doing behind the scenes)
   - Create dramatic irony: the reader knows the detective is wrong, but can only watch helplessly

5. **SUSPENSE BUILDING**:
   - Whenever the detective approaches the truth, something unexpected makes them turn in the wrong direction
   - The conspirators' interventions should be natural and seamless
   - Make the reader feel tense and frustrated

6. **CHARACTER DEVELOPMENT**:
   - Give each character distinctive mannerisms and speech patterns
   - The detective should be flesh and blood, making the reader sympathize with their predicament
   - The conspirators should perform flawlessly

7. **PURE NARRATIVE PROSE**:
   - No meta-commentary
   - No "Plot Point 1" type labels
   - Write like a published literary thriller

## FORMAT:

## Chapter {chapter_num}: [Your Creative Chapter Title]

[Chapter text...]

---

Now write Chapter {chapter_num}:"""

        chapter_response = llm.generate(
            prompt=chapter_prompt,
            max_new_tokens=6000,
            temperature=0.8,
        )

        chapter_text = llm._strip_thinking_tags(chapter_response.text)
        sections.append("\n\n" + chapter_text)

    # Step 3: Generate epilogue
    logger.info("\n[3/3] Generating epilogue...")

    epilogue_prompt = f"""Write a memorable epilogue for this mystery novel.

## STORY SUMMARY:
{concept_text[:2000]}...

## EPILOGUE REQUIREMENTS (800-1200 words):

1. **TIME JUMP**: Begin weeks or months after the truth was revealed

2. **THE PRICE OF JUSTICE**:
   - The fate of the real criminal and conspirators - legal punishment, social condemnation, or inner torment
   - Some confess and face justice, some still evade, some choose extreme measures
   - Show their "after" - prison life, exile abroad, or complete breakdown

3. **VICTIMS AND SURVIVORS**:
   - How the wrongly accused scapegoat rebuilds their life
   - The victim's family finding closure or still bearing unhealed wounds
   - How those innocently caught up continue forward

4. **THE DETECTIVE'S REFLECTION**:
   - The detective looks back on the entire case - those moments they were almost deceived
   - What ultimately made them see through to the truth?
   - Their insight into this case, their understanding of the dark side of human nature

5. **CLOSING IMAGE**:
   - End with a powerful image
   - Suggest that justice, though delayed, arrives, or that the weight of truth never dissipates
   - Let the reader feel relief tinged with gravity

6. **TONE**:
   - Literary, contemplative, with a sense of resolution
   - Like the calm after a storm, sunlight breaking through clouds
   - Lingering resonance, but this time with a note of hope

## FORMAT:

## Epilogue

[Epilogue text...]

Now write the epilogue:"""

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
