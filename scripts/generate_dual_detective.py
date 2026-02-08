#!/usr/bin/env python3
"""
Dual Detective story generation script.
One detective is real, one is the killer in disguise.
The killer-detective misleads the real detective throughout the investigation.
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


def generate_dual_detective_story(llm, num_chapters: int = 10) -> str:
    """Generate a mystery novel with two detectives - one real, one killer."""

    sections = []

    # Step 1: Generate the complete story concept, title, and prologue
    logger.info("\n[1/3] Generating story concept, title, and prologue...")

    concept_prompt = """You are an award-winning mystery novelist. Create a complete crime mystery novel with a unique twist.

## THE CORE PREMISE:

Two detectives are assigned to investigate a murder case together. What no one knows - except the reader - is that ONE OF THE DETECTIVES IS THE KILLER.

The killer-detective uses their position to:
- Mislead the investigation away from themselves
- Plant false evidence pointing to innocent suspects
- Sabotage crucial leads that might expose them
- Gain the trust of the real detective while manipulating them
- Stay one step ahead by knowing exactly what the investigation discovers

## STRUCTURAL REQUIREMENTS:

1. **THE TWO DETECTIVES**:
   - DETECTIVE A (The Real Detective): Skilled, dedicated, but trusts their partner
   - DETECTIVE B (The Killer-Detective): Appears equally dedicated, but secretly committed the murder and is now controlling the investigation from within

2. **DUAL PERSPECTIVE FOR THE READER**:
   - The reader knows from the beginning that Detective B is the killer
   - The reader watches Detective A being systematically deceived by their own partner
   - Every "helpful" suggestion from Detective B is actually misdirection
   - The reader sees both the surface (partnership) and the truth (manipulation)

3. **THE CRIME**:
   - A murder that Detective B committed for personal reasons (revenge, greed, passion, etc.)
   - Detective B either volunteered for the case or was coincidentally assigned
   - The perfect cover: investigating your own crime

4. **SUSPENSE MECHANISM**:
   - Detective A occasionally gets close to the truth
   - Detective B must subtly redirect without arousing suspicion
   - The reader feels the tension of near-discoveries
   - Cat-and-mouse dynamic where both are hunting - but for different reasons

5. **ENDING**:
   - Detective A eventually discovers the truth about their partner
   - The revelation is dramatic and personal - a betrayal of trust
   - Confrontation between the two detectives
   - Justice is served (or nearly served)

## YOUR TASK:

Create:
1. **NOVEL TITLE**: Evocative, hinting at duality, partnership, or hidden identity
2. **PROLOGUE (800-1200 words)**:
   - Show Detective B committing or immediately after committing the murder
   - Reveal their motive to the reader
   - Show them deciding to insert themselves into the investigation
   - End with them meeting Detective A as "partners"

## FORMAT:

```
# [Your Creative Novel Title]

*A Mystery Novel*

---

## Prologue: [Prologue Title]

[Prologue showing the murder and Detective B's decision to join the investigation...]

---

## Story Settings

**The Murder**: [What happened, where, when]
**The Victim**: [Name] - [Who they were] - [Connection to Detective B]
**Detective A (Real Detective)**: [Name] - [Personality, skills, vulnerabilities]
**Detective B (Killer-Detective)**: [Name] - [Public persona vs. true nature] - [Motive for the murder]
**The Scapegoat**: [Who Detective B plans to frame]
**Key Evidence**: [What could expose Detective B if found]
**The Partnership Dynamic**: [How they work together, why A trusts B]
```

Begin creating now:"""

    response = llm.generate(
        prompt=concept_prompt,
        max_new_tokens=4096,
        temperature=0.9,
    )

    concept_text = llm._strip_thinking_tags(response.text)
    sections.append(concept_text)

    logger.info("Parsing story settings...")

    # Step 2: Generate chapters
    logger.info(f"\n[2/3] Generating {num_chapters} chapters...")

    for chapter_num in range(1, num_chapters + 1):
        logger.info(f"  Writing Chapter {chapter_num}/{num_chapters}...")

        # Determine chapter focus based on position
        if chapter_num == 1:
            chapter_focus = """PARTNERSHIP BEGINS: Detective A and Detective B are assigned to the case together.
            Show their first interactions - A sees a capable partner, the reader sees a killer hiding in plain sight.
            They examine the crime scene together. B subtly steers A away from anything incriminating."""
        elif chapter_num == 2:
            chapter_focus = """BUILDING TRUST: The detectives interview witnesses and gather evidence.
            B provides "insights" that seem helpful but actually misdirect.
            A begins to rely on B's judgment. The reader watches the manipulation unfold."""
        elif chapter_num == 3:
            chapter_focus = """FIRST MISDIRECTION: B plants or highlights evidence pointing to an innocent suspect.
            A follows the false lead. B pretends to support while secretly relieved.
            Show B's internal satisfaction while maintaining their helpful facade."""
        elif chapter_num == 4:
            chapter_focus = """CLOSE CALL: A stumbles onto something that could expose B.
            B must think fast - they redirect, distract, or "accidentally" destroy evidence.
            The reader's tension peaks as B narrowly avoids exposure."""
        elif chapter_num == 5:
            chapter_focus = """DEEPENING BOND: A and B share personal moments - meals, conversations, trust-building.
            A opens up to B. B uses this to understand A's weaknesses.
            The reader sees the tragic irony of this false friendship."""
        elif chapter_num == 6:
            chapter_focus = """THE FRAME TIGHTENS: Evidence against the scapegoat mounts.
            B orchestrates the final pieces. A is convinced they've found the killer.
            The reader watches an innocent person being destroyed."""
        elif chapter_num == 7:
            chapter_focus = """DOUBT CREEPS IN: Something doesn't sit right with A.
            A small inconsistency, a gut feeling, a witness statement that doesn't match.
            B notices A's hesitation and works to reassure them."""
        elif chapter_num == 8:
            chapter_focus = """SECRET INVESTIGATION: A begins quietly investigating their own partner.
            A can't believe what they're finding. B doesn't know they're being watched.
            The tables are turning - now A is the one with secret knowledge."""
        elif chapter_num == 9:
            chapter_focus = """THE TRUTH EMERGES: A discovers undeniable proof that B is the killer.
            A's world shatters - their partner, their friend, is a murderer.
            A must decide how to proceed without alerting B."""
        else:
            chapter_focus = """CONFRONTATION: A confronts B with the truth.
            The masks come off. B may try to explain, justify, threaten, or escape.
            The partnership that defined the investigation becomes its climax.
            Justice is served - arrest, struggle, or dramatic conclusion."""

        chapter_prompt = f"""Continue writing Chapter {chapter_num} of this dual-detective mystery novel.

## STORY SUMMARY:
{concept_text[:3000]}...

## THIS CHAPTER'S FOCUS:
{chapter_focus}

## WRITING REQUIREMENTS:

1. **LENGTH**: 1500-2500 words of polished literary prose

2. **DUAL PERSPECTIVE**:
   - Show scenes from Detective A's perspective (trusting, investigating)
   - Show the reader what Detective B is really thinking/doing
   - Use dramatic irony: the reader knows B is the killer, A doesn't

3. **PARTNERSHIP DYNAMICS**:
   - Show realistic detective partnership (discussing leads, bouncing ideas)
   - B's suggestions should seem helpful on the surface
   - The reader should see the manipulation beneath

4. **PSYCHOLOGICAL DEPTH**:
   - A's growing trust (and eventual suspicion)
   - B's constant performance, the stress of maintaining the facade
   - The reader's frustration watching A be deceived

5. **DIALOGUE**:
   - Natural partnership banter
   - B's dialogue should have double meanings the reader catches
   - A's questions that accidentally get too close to the truth

6. **TENSION BUILDING**:
   - Near-misses where A almost discovers the truth
   - B's quick thinking to deflect
   - Moments where B's mask almost slips

7. **SENSORY DETAILS**:
   - Crime scenes, interrogation rooms, late-night stake-outs
   - The physical presence of both detectives
   - B's micro-expressions that A misses but the reader catches

8. **PURE NARRATIVE PROSE**:
   - No meta-commentary or labels
   - Write like a published psychological thriller

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

    epilogue_prompt = f"""Write a memorable epilogue for this dual-detective mystery novel.

## STORY SUMMARY:
{concept_text[:2000]}...

## EPILOGUE REQUIREMENTS (800-1200 words):

1. **AFTERMATH**:
   - Detective B's fate - arrest, trial, prison, or other conclusion
   - The scapegoat cleared, their life beginning to rebuild
   - The victim's family finding closure

2. **DETECTIVE A'S RECKONING**:
   - Processing the betrayal by someone they trusted
   - Questioning their judgment - how did they miss the signs?
   - The psychological weight of having worked alongside the killer
   - Whether they can ever trust a partner again

3. **REFLECTION ON THE PARTNERSHIP**:
   - A looks back on specific moments now seen in new light
   - Those times B "helped" that were actually manipulation
   - The conversations that now feel sinister
   - Small kindnesses that were calculated moves

4. **THE FINAL IMAGE**:
   - Perhaps A visiting B in prison, or choosing never to see them again
   - A returning to work, forever changed
   - A symbol that captures the duality of the experience

5. **TONE**:
   - Contemplative, melancholic, but with resolution
   - The weight of betrayal balanced with justice achieved
   - A forever altered by this experience

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
    """Generate a dual-detective mystery novel."""
    logger.info("=" * 60)
    logger.info("SMOKEMIRROR - DUAL DETECTIVE MODE")
    logger.info("=" * 60)
    logger.info("One detective is real. One is the killer.")
    logger.info("=" * 60)

    from src.utils.config import load_config
    from src.models.llm_wrapper import create_llm_wrapper

    # Load 32B config
    config = load_config(str(project_root / "configs" / "test_32b.yaml"))
    config.set_seed()

    logger.info(f"Model: {config.model.name}")
    logger.info("Mode: DUAL DETECTIVE (killer as partner)")

    # Initialize LLM
    logger.info("\nLoading model...")
    llm = create_llm_wrapper(config.model, use_mock=False)

    # Generate story
    logger.info("\n" + "=" * 60)
    logger.info("GENERATING STORY...")
    logger.info("=" * 60)

    story = generate_dual_detective_story(llm, num_chapters=10)

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
