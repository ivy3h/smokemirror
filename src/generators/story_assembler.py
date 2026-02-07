"""
Story Assembler

Assembles plot points into a cohesive narrative with proper prose.
"""

import logging
import re
from typing import Optional

from ..models.llm_wrapper import LLMWrapper
from ..data_structures.facts import (
    CrimeFacts,
    FabricatedFacts,
    PlotPoint,
    StoryState,
)
from ..utils.prompts import PromptTemplates

logger = logging.getLogger(__name__)


class StoryAssembler:
    """Assembles generated plot points into a polished narrative."""

    def __init__(self, llm: LLMWrapper, use_thinking: bool = False):
        """Initialize the assembler.

        Args:
            llm: LLM wrapper for generation
            use_thinking: Whether to enable thinking mode (for larger models like 32B)
        """
        self.llm = llm
        self.use_thinking = use_thinking

    def _strip_thinking_tags(self, text: str) -> str:
        """Remove Qwen3 thinking tags from text."""
        text = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.MULTILINE)
        text = re.sub(r"<think>[\s\S]*$", "", text, flags=re.MULTILINE)
        return text.strip()

    def assemble(
        self,
        plot_points: list[PlotPoint],
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
        include_reader_perspective: bool = True,
    ) -> str:
        """Assemble plot points into a complete narrative.

        Uses chapter-by-chapter generation for better coherence.

        Args:
            plot_points: List of plot points to assemble
            real_facts: Real crime facts for reader revelations
            fabricated_facts: Fabricated narrative
            include_reader_perspective: Whether to include reader-facing revelations

        Returns:
            Complete story as markdown string
        """
        logger.info(f"Assembling {len(plot_points)} plot points into narrative")

        sections = []

        # Title
        sections.append("# The Dual Narrative\n\n")
        sections.append("*A Crime Mystery*\n\n")
        sections.append("---\n\n")

        # Prologue: What the reader knows (written directly, not by LLM)
        if include_reader_perspective:
            sections.append("## Prologue: The Truth Behind the Smoke\n\n")
            sections.append("*The reader knows what the detective does not...*\n\n")
            sections.append(
                f"On the night of the crime, {real_facts.criminal.name} "
                f"committed {real_facts.crime_type}. "
                f"The victim was {real_facts.victim.name}, "
                f"a {real_facts.victim.occupation}. "
                f"The motive: {real_facts.motive}.\n\n"
            )
            sections.append(
                f"But {real_facts.criminal.name} did not act alone. "
                f"A network of conspirators—{', '.join([c.name for c in real_facts.conspirators])}—"
                f"helped construct an elaborate false narrative. "
                f"Their plan: {real_facts.coordination_plan}.\n\n"
            )
            sections.append(
                f"As the detective begins the investigation, "
                f"the reader watches, knowing the truth, "
                f"as every clue points in the wrong direction...\n\n"
            )
            sections.append("---\n\n")

        # Generate chapters (3-5 plot points each)
        chapter_size = 5
        chapter_titles = [
            "The Discovery",
            "Following the Trail",
            "Smoke and Mirrors",
            "The Web Tightens",
            "Closing In",
            "The Final Deception",
        ]

        previous_summary = f"Detective begins investigating the {real_facts.crime_type} of {real_facts.victim.name}."

        for i in range(0, len(plot_points), chapter_size):
            chapter_num = i // chapter_size + 1
            chapter_points = plot_points[i:i + chapter_size]
            title_idx = min(chapter_num - 1, len(chapter_titles) - 1)

            chapter_text = self._generate_chapter_prose(
                chapter_num=chapter_num,
                chapter_title=chapter_titles[title_idx],
                plot_points=chapter_points,
                real_facts=real_facts,
                fabricated_facts=fabricated_facts,
                previous_summary=previous_summary,
            )

            sections.append(chapter_text)
            sections.append("\n\n---\n\n")

            # Update summary for next chapter
            if chapter_points:
                previous_summary = f"The detective {chapter_points[-1].description}"

        # Epilogue
        sections.append("## Epilogue\n\n")
        epilogue = self._generate_epilogue(real_facts, fabricated_facts, plot_points)
        sections.append(epilogue)

        return "".join(sections)

    def _generate_chapter_prose(
        self,
        chapter_num: int,
        chapter_title: str,
        plot_points: list[PlotPoint],
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
        previous_summary: str,
    ) -> str:
        """Generate flowing prose for a single chapter."""

        # Build plot point descriptions
        events = []
        for pp in plot_points:
            event = pp.description
            if pp.conspirator_intervention:
                event += f" ({pp.conspirator_intervention})"
            if pp.detective_learns:
                event += f" The detective learns: {pp.detective_learns}."
            events.append(event)

        events_text = "\n".join(f"- {e}" for e in events)

        prompt = f"""Write Chapter {chapter_num}: "{chapter_title}" of a mystery novel.

STORY CONTEXT:
- Detective is investigating the {real_facts.crime_type} of {real_facts.victim.name}
- The real criminal is {real_facts.criminal.name} (reader knows this, detective doesn't)
- The detective is being misled to suspect {fabricated_facts.fake_suspect.name}
- Previous: {previous_summary}

EVENTS TO COVER IN THIS CHAPTER:
{events_text}

WRITING REQUIREMENTS:
1. Write in third person, past tense, like a published mystery novel
2. Create flowing prose with natural dialogue and scene descriptions
3. Show the detective's thought process as they follow false leads
4. Build suspense - the reader knows the truth but watches the detective be misled
5. Include sensory details: sights, sounds, atmosphere
6. DO NOT use headers like "Plot Point 1" - write continuous narrative prose
7. Each chapter should be 400-600 words of engaging fiction

Write the chapter now (prose only, no meta-commentary):"""

        response = self.llm.generate(
            prompt=prompt,
            max_new_tokens=4096,
            temperature=0.8,
            disable_thinking=not self.use_thinking,
        )

        # Clean up response (strip thinking tags if thinking mode was used)
        chapter_text = self._strip_thinking_tags(response.text) if self.use_thinking else response.text

        # Remove any accidental headers or meta-text
        chapter_text = re.sub(r"^\*\*?(Chapter|CHAPTER).*?\*\*?\n*", "", chapter_text)
        chapter_text = re.sub(r"^(Plot Point|PLOT POINT).*?\n", "", chapter_text, flags=re.MULTILINE)

        return f"## Chapter {chapter_num}: {chapter_title}\n\n{chapter_text.strip()}"

    def _generate_epilogue(
        self,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
        plot_points: list[PlotPoint],
    ) -> str:
        """Generate the epilogue showing the conspiracy's success."""

        prompt = f"""Write a short epilogue (200-300 words) for this mystery novel.

THE TRUTH:
- {real_facts.criminal.name} committed {real_facts.crime_type}
- Conspirators {', '.join([c.name for c in real_facts.conspirators])} helped cover it up
- The detective was misled to suspect {fabricated_facts.fake_suspect.name}

ENDING:
The conspiracy succeeded. The wrong person was suspected. Show:
1. The conspirators reflecting on their successful deception
2. The real criminal feeling safe, knowing they got away with it
3. A final dramatic irony - the truth the reader knows but justice missed

Write in third person past tense. Atmospheric and haunting tone. No headers or meta-text:"""

        response = self.llm.generate(
            prompt=prompt,
            max_new_tokens=4096,
            temperature=0.8,
            disable_thinking=not self.use_thinking,
        )

        text = self._strip_thinking_tags(response.text) if self.use_thinking else response.text
        return text.strip()

    def _format_plot_points(self, plot_points: list[PlotPoint]) -> str:
        """Format plot points for the assembly prompt.

        Args:
            plot_points: List of plot points

        Returns:
            Formatted string
        """
        formatted = []
        for pp in plot_points:
            entry = f"Plot Point {pp.id}:\n"
            entry += f"  Description: {pp.description}\n"
            if pp.detective_action:
                entry += f"  Detective Action: {pp.detective_action}\n"
            if pp.conspirator_intervention:
                entry += f"  Conspirator Intervention: {pp.conspirator_intervention}\n"
            if pp.obstacle:
                entry += f"  Obstacle: {pp.obstacle}\n"
            if pp.reader_revelation:
                entry += f"  [READER KNOWS: {pp.reader_revelation}]\n"
            if pp.detective_learns:
                entry += f"  Detective Learns: {pp.detective_learns}\n"
            entry += f"  Suspense Level: {pp.suspense_level}/10\n"
            formatted.append(entry)

        return "\n".join(formatted)

    def _create_crime_summary(
        self,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ) -> str:
        """Create a summary of the crime for reader context.

        Args:
            real_facts: Real crime facts
            fabricated_facts: Fabricated narrative

        Returns:
            Crime summary string
        """
        summary = f"""
THE TRUTH (known to the reader):
- Crime: {real_facts.crime_type}
- Victim: {real_facts.victim.name} ({real_facts.victim.occupation})
- Real Criminal: {real_facts.criminal.name} ({real_facts.criminal.occupation})
- Motive: {real_facts.motive}
- Method: {real_facts.method}
- Conspirators: {', '.join([c.name for c in real_facts.conspirators])}
- Their Plan: {real_facts.coordination_plan}

THE LIE (what the detective sees):
- Fake Suspect: {fabricated_facts.fake_suspect.name}
- Fabricated Motive: {fabricated_facts.fake_motive}
- Cover Story: {fabricated_facts.cover_story}
"""
        return summary

    def _format_narrative(
        self,
        raw_narrative: str,
        plot_points: list[PlotPoint],
        real_facts: CrimeFacts,
        include_reader_perspective: bool,
    ) -> str:
        """Format the narrative with proper structure.

        Args:
            raw_narrative: Raw generated narrative
            plot_points: Original plot points
            real_facts: Real crime facts
            include_reader_perspective: Whether to include reader sections

        Returns:
            Formatted markdown narrative
        """
        # Build the formatted story
        sections = []

        # Title and prologue
        sections.append("# The Dual Narrative\n")
        sections.append("*A Crime Mystery*\n\n")
        sections.append("---\n\n")

        # Prologue: What the reader knows
        if include_reader_perspective:
            sections.append("## Prologue: The Truth Behind the Smoke\n\n")
            sections.append(f"*The reader knows what the detective does not...*\n\n")
            sections.append(
                f"On the night of the crime, {real_facts.criminal.name} "
                f"committed {real_facts.crime_type}. "
                f"The victim was {real_facts.victim.name}, "
                f"a {real_facts.victim.occupation}. "
                f"The motive: {real_facts.motive}.\n\n"
            )
            sections.append(
                f"But {real_facts.criminal.name} did not act alone. "
                f"A network of conspirators—{', '.join([c.name for c in real_facts.conspirators])}—"
                f"helped construct an elaborate false narrative. "
                f"Their plan: {real_facts.coordination_plan}.\n\n"
            )
            sections.append(
                f"As the detective begins the investigation, "
                f"the reader watches, knowing the truth, "
                f"as every clue points in the wrong direction...\n\n"
            )
            sections.append("---\n\n")

        # Main narrative
        sections.append("## The Investigation\n\n")
        sections.append(raw_narrative)

        # Add resolution section if we have enough plot points
        if len(plot_points) >= 15:
            sections.append("\n\n---\n\n")
            sections.append("## Resolution\n\n")
            sections.append(
                "*The story reaches its conclusion as the detective "
                "approaches the final truth—or continues to be misled...*\n\n"
            )

        return "".join(sections)

    def generate_chapter(
        self,
        plot_points: list[PlotPoint],
        chapter_title: str,
        previous_context: Optional[str] = None,
    ) -> str:
        """Generate a single chapter from a subset of plot points.

        Args:
            plot_points: Plot points for this chapter
            chapter_title: Title of the chapter
            previous_context: Summary of previous chapters

        Returns:
            Chapter text
        """
        context = previous_context or "This is the beginning of the story."

        prompt = f"""Write a chapter titled "{chapter_title}" for a mystery story.

PREVIOUS CONTEXT:
{context}

PLOT POINTS FOR THIS CHAPTER:
{self._format_plot_points(plot_points)}

Write the chapter in engaging prose. Build suspense. Include dialogue where appropriate.
The reader knows more than the detective—use this for dramatic irony.

Chapter:"""

        response = self.llm.generate(
            prompt=prompt,
            max_new_tokens=2048,
            temperature=0.8,
        )

        return f"## {chapter_title}\n\n{response.text}"

    def assemble_with_chapters(
        self,
        plot_points: list[PlotPoint],
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
        chapter_size: int = 5,
    ) -> str:
        """Assemble story with chapter divisions.

        Args:
            plot_points: All plot points
            real_facts: Real crime facts
            fabricated_facts: Fabricated narrative
            chapter_size: Number of plot points per chapter

        Returns:
            Complete chaptered narrative
        """
        sections = []

        # Title and prologue
        sections.append("# The Dual Narrative\n\n")
        sections.append("*A Crime Mystery*\n\n")
        sections.append("---\n\n")

        # Prologue
        sections.append("## Prologue\n\n")
        sections.append(
            f"The body of {real_facts.victim.name} was discovered on a cold morning. "
            f"What appeared to be a straightforward case would soon reveal layers of deception...\n\n"
        )

        # Generate chapters
        chapter_num = 1
        previous_context = "The investigation has just begun."

        for i in range(0, len(plot_points), chapter_size):
            chapter_points = plot_points[i : i + chapter_size]

            chapter_titles = [
                "The Discovery",
                "False Trails",
                "Smoke and Mirrors",
                "The Web Tightens",
                "Approaching the Truth",
            ]
            title = chapter_titles[min(chapter_num - 1, len(chapter_titles) - 1)]

            chapter = self.generate_chapter(
                chapter_points,
                f"Chapter {chapter_num}: {title}",
                previous_context,
            )
            sections.append(chapter)
            sections.append("\n\n---\n\n")

            # Update context for next chapter
            previous_context = f"In the previous chapter, the detective {chapter_points[-1].description}"
            chapter_num += 1

        return "".join(sections)

    def generate_summary(
        self,
        plot_points: list[PlotPoint],
        real_facts: CrimeFacts,
    ) -> str:
        """Generate a brief summary of the story.

        Args:
            plot_points: All plot points
            real_facts: Real crime facts

        Returns:
            Story summary
        """
        prompt = f"""Summarize this mystery story in 3-4 paragraphs:

CRIME: {real_facts.crime_type}
VICTIM: {real_facts.victim.name}
REAL CRIMINAL: {real_facts.criminal.name}
CONSPIRATORS: {', '.join([c.name for c in real_facts.conspirators])}

KEY PLOT POINTS:
{self._format_plot_points(plot_points[:5])}
...
{self._format_plot_points(plot_points[-3:])}

Provide a compelling summary that captures the suspense and dual-narrative structure:"""

        response = self.llm.generate(prompt, max_new_tokens=512)
        return response.text
