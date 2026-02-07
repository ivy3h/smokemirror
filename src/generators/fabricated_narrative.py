"""
Fabricated Narrative Generator

Generates the false narrative that conspirators create to mislead the detective.
"""

import logging
import json
from typing import Optional

from ..models.llm_wrapper import LLMWrapper
from ..data_structures.facts import (
    Character,
    CharacterRole,
    Evidence,
    EvidenceType,
    Timeline,
    CrimeFacts,
    FabricatedFacts,
)
from ..utils.prompts import PromptTemplates

logger = logging.getLogger(__name__)


class ConsistencyValidator:
    """Non-neural validator for checking consistency between real and fabricated facts."""

    def __init__(self):
        self.issues = []

    def validate(
        self,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ) -> tuple[bool, list[str]]:
        """Validate consistency between real and fabricated narratives.

        Args:
            real_facts: The real crime facts
            fabricated_facts: The fabricated narrative

        Returns:
            Tuple of (is_valid, list of issues)
        """
        self.issues = []

        # Check that all real evidence has a fabricated explanation
        self._check_evidence_coverage(real_facts, fabricated_facts)

        # Check timeline plausibility
        self._check_timeline_plausibility(real_facts, fabricated_facts)

        # Check alibi consistency
        self._check_alibi_consistency(real_facts, fabricated_facts)

        # Check that fake suspect is different from real criminal
        self._check_suspect_distinct(real_facts, fabricated_facts)

        return len(self.issues) == 0, self.issues

    def _check_evidence_coverage(
        self,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ):
        """Check that all real evidence has a fabricated explanation."""
        real_evidence_ids = {e.id for e in real_facts.evidence}
        explained_evidence = set()

        # Check planted evidence explains real evidence
        for pe in fabricated_facts.planted_evidence:
            if pe.fabricated_meaning:
                explained_evidence.add(pe.id)

        # Also check if evidence_explanations covers remaining
        # (This would be in the fabricated facts JSON)

        uncovered = real_evidence_ids - explained_evidence
        if uncovered:
            self.issues.append(
                f"Real evidence not explained in fabricated narrative: {uncovered}"
            )

    def _check_timeline_plausibility(
        self,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ):
        """Check that fabricated timeline doesn't contradict verifiable facts."""
        # Basic check: fabricated timeline should have similar timeframe
        if not fabricated_facts.fake_timeline.events:
            self.issues.append("Fabricated timeline is empty")
            return

        # Could add more sophisticated time parsing and validation here

    def _check_alibi_consistency(
        self,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ):
        """Check that conspirator alibis don't conflict with each other."""
        alibis = fabricated_facts.alibis

        # Check all conspirators have alibis
        for conspirator in real_facts.conspirators:
            if conspirator.name not in alibis:
                self.issues.append(f"Missing alibi for conspirator: {conspirator.name}")

    def _check_suspect_distinct(
        self,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ):
        """Check that fake suspect is not the real criminal."""
        if fabricated_facts.fake_suspect.name == real_facts.criminal.name:
            self.issues.append(
                "Fake suspect is the same as the real criminal - defeats the purpose!"
            )


class FabricatedNarrativeGenerator:
    """Generates the fabricated crime narrative that conspirators create."""

    def __init__(self, llm: LLMWrapper):
        """Initialize the generator.

        Args:
            llm: LLM wrapper for generation
        """
        self.llm = llm
        self.validator = ConsistencyValidator()

    def generate(
        self,
        real_facts: CrimeFacts,
        max_retries: int = 3,
    ) -> FabricatedFacts:
        """Generate the fabricated narrative based on real facts.

        Args:
            real_facts: The real crime facts
            max_retries: Maximum attempts to generate valid fabrication

        Returns:
            FabricatedFacts object
        """
        logger.info("Generating fabricated narrative")

        # Convert real facts to string for prompt
        real_facts_str = json.dumps(real_facts.to_dict(), indent=2)

        for attempt in range(max_retries):
            prompt = PromptTemplates.FABRICATED_NARRATIVE_PROMPT.format(
                real_facts=real_facts_str
            )

            response = self.llm.generate_with_retry(
                prompt=prompt,
                system_prompt=PromptTemplates.FABRICATED_NARRATIVE_SYSTEM,
                expect_json=True,
            )

            if not response.success or response.parsed_json is None:
                logger.warning(f"Generation attempt {attempt + 1} failed")
                continue

            fabricated_facts = self._parse_fabricated_facts(response.parsed_json)

            # Validate consistency
            is_valid, issues = self.validator.validate(real_facts, fabricated_facts)

            if is_valid:
                return fabricated_facts

            logger.warning(f"Validation failed: {issues}. Retrying...")

            # Try to fix issues
            fabricated_facts = self._fix_issues(
                real_facts, fabricated_facts, issues
            )

            # Re-validate
            is_valid, remaining_issues = self.validator.validate(
                real_facts, fabricated_facts
            )
            if is_valid:
                return fabricated_facts

        # Return best effort if all retries fail
        logger.warning("Returning fabricated narrative with potential issues")
        return fabricated_facts

    def _parse_fabricated_facts(self, data: dict) -> FabricatedFacts:
        """Parse JSON response into FabricatedFacts structure.

        Args:
            data: Parsed JSON data

        Returns:
            FabricatedFacts object
        """
        # Parse fake suspect
        suspect_data = data.get("fake_suspect", {})
        fake_suspect = Character(
            name=suspect_data.get("name", "Unknown Suspect"),
            role=CharacterRole.SUSPECT,
            occupation=suspect_data.get("occupation", "Unknown"),
            motive=suspect_data.get("fake_motive", "Unknown motive"),
            means=suspect_data.get("fake_means", "Unknown means"),
            opportunity=suspect_data.get("fake_opportunity", "Unknown opportunity"),
        )

        # Parse fake timeline
        fake_timeline = Timeline()
        for event in data.get("fake_timeline", []):
            fake_timeline.add_event(
                time=event.get("time", "Unknown"),
                description=event.get("event", "Unknown event"),
                actor=event.get("actor", "Unknown"),
                location=event.get("location", "Unknown"),
            )

        # Parse planted evidence
        planted_evidence = []
        for e_data in data.get("planted_evidence", []):
            evidence = Evidence(
                id=e_data.get("id", f"PE{len(planted_evidence)}"),
                description=e_data.get("description", "Unknown evidence"),
                evidence_type=self._parse_evidence_type(e_data.get("type", "physical")),
                location=e_data.get("location", "Unknown"),
                is_planted=True,
                fabricated_meaning=e_data.get("fabricated_meaning", "Unknown meaning"),
            )
            planted_evidence.append(evidence)

        # Parse alibis
        alibis = data.get("alibis", {})

        # Parse cover story
        cover_story = data.get("cover_story", "No cover story provided")

        return FabricatedFacts(
            fake_suspect=fake_suspect,
            fake_motive=fake_suspect.motive or data.get("fake_motive", "Unknown"),
            fake_method=data.get("fake_method", "Unknown method"),
            fake_timeline=fake_timeline,
            planted_evidence=planted_evidence,
            alibis=alibis,
            cover_story=cover_story,
        )

    def _parse_evidence_type(self, type_str: str) -> EvidenceType:
        """Parse evidence type string to enum."""
        type_map = {
            "physical": EvidenceType.PHYSICAL,
            "testimonial": EvidenceType.TESTIMONIAL,
            "documentary": EvidenceType.DOCUMENTARY,
            "digital": EvidenceType.DIGITAL,
            "circumstantial": EvidenceType.CIRCUMSTANTIAL,
        }
        return type_map.get(type_str.lower(), EvidenceType.PHYSICAL)

    def _fix_issues(
        self,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
        issues: list[str],
    ) -> FabricatedFacts:
        """Attempt to fix consistency issues.

        Args:
            real_facts: The real crime facts
            fabricated_facts: The current fabricated facts
            issues: List of issues to fix

        Returns:
            Updated FabricatedFacts
        """
        # Generate fixes for specific issues
        fix_prompt = f"""The following fabricated narrative has consistency issues that need to be fixed:

FABRICATED NARRATIVE:
{json.dumps(fabricated_facts.to_dict(), indent=2)}

ISSUES TO FIX:
{json.dumps(issues)}

REAL CRIME FACTS (for reference):
Crime type: {real_facts.crime_type}
Evidence that must be explained: {[e.description for e in real_facts.evidence]}
Conspirators needing alibis: {[c.name for c in real_facts.conspirators]}

Provide fixes in JSON format:
{{
    "fixed_alibis": {{"conspirator_name": "fixed alibi"}},
    "evidence_explanations": {{"evidence_id": "how this fits fabricated story"}},
    "additional_planted_evidence": [...]
}}"""

        response = self.llm.generate_with_retry(
            prompt=fix_prompt,
            expect_json=True,
        )

        if response.parsed_json:
            fixes = response.parsed_json

            # Apply fixed alibis
            if "fixed_alibis" in fixes:
                fabricated_facts.alibis.update(fixes["fixed_alibis"])

            # Could add more fix applications here

        return fabricated_facts

    def generate_evidence_explanations(
        self,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ) -> dict[str, str]:
        """Generate explanations for how real evidence fits the fabricated story.

        Args:
            real_facts: Real crime facts
            fabricated_facts: Fabricated narrative

        Returns:
            Dict mapping evidence ID to fabricated explanation
        """
        explanations = {}

        for evidence in real_facts.evidence:
            prompt = f"""How would conspirators explain this evidence to fit their fabricated story?

EVIDENCE: {evidence.description}
REAL MEANING: {evidence.real_meaning}
FABRICATED STORY: {fabricated_facts.cover_story}
FAKE SUSPECT: {fabricated_facts.fake_suspect.name}

Provide a brief explanation that makes this evidence point to the fake suspect:"""

            response = self.llm.generate(prompt)
            explanations[evidence.id] = response.text.strip()

        return explanations
