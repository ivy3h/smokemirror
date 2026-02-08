"""
Crime Backstory Generator

Generates the real crime facts including criminal, victim, conspirators,
method, timeline, and evidence.
"""

import logging
import random
from typing import Optional

from ..models.llm_wrapper import LLMWrapper, LLMResponse
from ..data_structures.facts import (
    Character,
    CharacterRole,
    Evidence,
    EvidenceType,
    Timeline,
    CrimeFacts,
    DiscoveryPath,
)
from ..utils.prompts import PromptTemplates
from ..utils.config import GenerationConfig

logger = logging.getLogger(__name__)


# Pre-defined settings for variety
CRIME_TYPES = ["murder", "embezzlement", "art theft", "corporate sabotage", "kidnapping"]
SETTINGS = [
    "tech startup",
    "law firm",
    "art gallery",
    "luxury hotel",
    "pharmaceutical company",
    "investment bank",
    "university",
    "theater company",
]
MOTIVES = [
    "financial gain",
    "revenge",
    "cover-up of previous crime",
    "jealousy",
    "power struggle",
    "blackmail gone wrong",
    "inheritance",
    "professional rivalry",
]


class CrimeBackstoryGenerator:
    """Generates detailed crime backstories for mystery stories."""

    def __init__(self, llm: LLMWrapper, config: GenerationConfig):
        """Initialize the generator.

        Args:
            llm: LLM wrapper for generation
            config: Generation configuration
        """
        self.llm = llm
        self.config = config

    def generate(
        self,
        crime_type: Optional[str] = None,
        setting: Optional[str] = None,
        num_conspirators: Optional[int] = None,
    ) -> tuple[CrimeFacts, list[DiscoveryPath]]:
        """Generate a complete crime backstory.

        Args:
            crime_type: Type of crime (or random if None)
            setting: Story setting (or random if None)
            num_conspirators: Number of conspirators (or random within config range)

        Returns:
            Tuple of (CrimeFacts, list of DiscoveryPaths)
        """
        # Select parameters
        crime_type = crime_type or random.choice(CRIME_TYPES)
        setting = setting or random.choice(SETTINGS)
        num_conspirators = num_conspirators or random.randint(
            self.config.min_conspirators, self.config.max_conspirators
        )

        logger.info(f"Generating crime backstory: {crime_type} in {setting}")

        # Generate the main crime details
        prompt = PromptTemplates.CRIME_BACKSTORY_PROMPT.format(
            crime_type=crime_type,
            num_conspirators=num_conspirators,
            setting=setting,
        )

        response = self.llm.generate_with_retry(
            prompt=prompt,
            system_prompt=PromptTemplates.CRIME_BACKSTORY_SYSTEM,
            expect_json=True,
            max_retries=3,
        )

        if not response.success or response.parsed_json is None:
            logger.error("Failed to generate crime backstory")
            # Return a minimal fallback
            return self._create_fallback_crime(crime_type, setting), []

        # Parse the response into structured data
        crime_facts = self._parse_crime_facts(response.parsed_json)

        # Validate complexity
        if not self._validate_complexity(crime_facts):
            logger.warning("Crime not complex enough, regenerating...")
            # Could retry here, but for now just proceed

        # Generate discovery paths
        discovery_paths = self._generate_discovery_paths(crime_facts)

        return crime_facts, discovery_paths

    def _parse_crime_facts(self, data: dict) -> CrimeFacts:
        """Parse JSON response into CrimeFacts structure.

        Args:
            data: Parsed JSON data

        Returns:
            CrimeFacts object
        """
        # Parse victim
        victim_data = data.get("victim", {})
        victim = Character(
            name=victim_data.get("name", "Unknown Victim"),
            role=CharacterRole.VICTIM,
            occupation=victim_data.get("occupation", "Unknown"),
            relationship_to_victim="self",
        )

        # Parse criminal
        criminal_data = data.get("criminal", {})
        criminal = Character(
            name=criminal_data.get("name", "Unknown Criminal"),
            role=CharacterRole.CRIMINAL,
            occupation=criminal_data.get("occupation", "Unknown"),
            motive=criminal_data.get("motive", "Unknown motive"),
            means=criminal_data.get("means", "Had the means"),
            opportunity=criminal_data.get("opportunity", "Had the opportunity"),
        )

        # Parse conspirators
        conspirators = []
        for c_data in data.get("conspirators", []):
            conspirator = Character(
                name=c_data.get("name", f"Conspirator_{len(conspirators)}"),
                role=CharacterRole.CONSPIRATOR,
                occupation=c_data.get("occupation", "Unknown"),
                leverage=c_data.get("leverage", "Unknown leverage"),
                alibi=c_data.get("alibi_provided", "Unknown alibi"),
                is_conspirator=True,
            )
            conspirators.append(conspirator)

        # Parse timeline
        timeline = Timeline()
        for event in data.get("timeline", []):
            timeline.add_event(
                time=event.get("time", "Unknown"),
                description=event.get("event", "Unknown event"),
                actor=event.get("actor", "Unknown"),
                location=event.get("location", "Unknown"),
            )

        # Parse evidence
        evidence_list = []
        for e_data in data.get("evidence", []):
            # Assign steps_required based on evidence type: physical/digital
            # evidence requires more investigation steps (multi-step clues)
            etype = e_data.get("type", "physical").lower()
            if etype in ("physical", "digital"):
                steps = random.randint(2, 3)
            elif etype == "documentary":
                steps = random.randint(1, 2)
            else:  # testimonial, circumstantial
                steps = 1

            evidence = Evidence(
                id=e_data.get("id", f"E{len(evidence_list)}"),
                description=e_data.get("description", "Unknown evidence"),
                evidence_type=self._parse_evidence_type(etype),
                location=e_data.get("location", "Unknown"),
                real_meaning=e_data.get("real_meaning", "Unknown meaning"),
                steps_required=steps,
            )
            evidence_list.append(evidence)

        return CrimeFacts(
            crime_type=data.get("crime_type", "unknown"),
            victim=victim,
            criminal=criminal,
            conspirators=conspirators,
            motive=criminal.motive or data.get("motive", "Unknown"),
            method=data.get("method", "Unknown method"),
            timeline=timeline,
            evidence=evidence_list,
            location=data.get("location", "Unknown location"),
            coordination_plan=data.get("coordination_plan", "Unknown coordination"),
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

    def _validate_complexity(self, crime_facts: CrimeFacts) -> bool:
        """Validate that the crime is complex enough.

        Args:
            crime_facts: The generated crime facts

        Returns:
            True if complex enough, False otherwise
        """
        # Check minimum requirements
        min_requirements = [
            len(crime_facts.conspirators) >= self.config.min_conspirators,
            len(crime_facts.evidence) >= 3,
            len(crime_facts.timeline.events) >= 4,
        ]
        return all(min_requirements)

    def _generate_discovery_paths(self, crime_facts: CrimeFacts) -> list[DiscoveryPath]:
        """Generate potential discovery paths for the detective.

        Args:
            crime_facts: The crime facts

        Returns:
            List of discovery paths
        """
        paths = []

        # Path through each conspirator (their testimony could crack)
        for conspirator in crime_facts.conspirators:
            paths.append(DiscoveryPath(
                id=f"path_conspirator_{conspirator.name}",
                description=f"Catch {conspirator.name} in a lie or contradiction",
                involves_character=conspirator.name,
                difficulty=random.randint(4, 8),
            ))

        # Path through evidence examination
        for evidence in crime_facts.evidence:
            paths.append(DiscoveryPath(
                id=f"path_evidence_{evidence.id}",
                description=f"Discover true meaning of {evidence.description}",
                involves_evidence=evidence.id,
                difficulty=random.randint(5, 9),
            ))

        # Path through timeline inconsistencies
        paths.append(DiscoveryPath(
            id="path_timeline",
            description="Notice timeline inconsistencies between conspirator accounts",
            difficulty=7,
        ))

        # Path through external witness
        paths.append(DiscoveryPath(
            id="path_external_witness",
            description="Find an unexpected witness who saw something",
            difficulty=6,
        ))

        # Ensure we have at least the configured number of paths
        while len(paths) < self.config.initial_discovery_paths:
            paths.append(DiscoveryPath(
                id=f"path_generic_{len(paths)}",
                description=f"Generic investigation path {len(paths)}",
                difficulty=random.randint(5, 8),
            ))

        return paths[:self.config.initial_discovery_paths + 3]  # Keep some extra

    def _create_fallback_crime(self, crime_type: str, setting: str) -> CrimeFacts:
        """Create a fallback crime if generation fails.

        Args:
            crime_type: Type of crime
            setting: Story setting

        Returns:
            Minimal CrimeFacts object
        """
        victim = Character(
            name="James Wilson",
            role=CharacterRole.VICTIM,
            occupation="Auditor",
        )

        criminal = Character(
            name="David Chen",
            role=CharacterRole.CRIMINAL,
            occupation="CFO",
            motive="Cover up embezzlement",
            means="Access to victim's schedule",
            opportunity="Late night meeting",
        )

        conspirator = Character(
            name="Alice",
            role=CharacterRole.CONSPIRATOR,
            occupation="Secretary",
            leverage="David knows about her past fraud",
            is_conspirator=True,
        )

        timeline = Timeline()
        timeline.add_event("8:00 PM", "Victim arrives at office", "James Wilson", "Office")
        timeline.add_event("9:00 PM", "Crime occurs", "David Chen", "Parking garage")
        timeline.add_event("9:30 PM", "Body discovered", "Alice", "Parking garage")

        evidence = [
            Evidence(
                id="E1",
                description="Security camera footage gap",
                evidence_type=EvidenceType.DIGITAL,
                location="Security office",
                real_meaning="Footage was deleted by conspirator",
            )
        ]

        return CrimeFacts(
            crime_type=crime_type,
            victim=victim,
            criminal=criminal,
            conspirators=[conspirator],
            motive="Cover up embezzlement",
            method="Staged accident in parking garage",
            timeline=timeline,
            evidence=evidence,
            location=setting,
            coordination_plan="Synchronized alibis and planted evidence",
        )

    def generate_additional_suspects(
        self,
        crime_facts: CrimeFacts,
        num_suspects: int = 2,
    ) -> list[Character]:
        """Generate additional innocent suspects.

        Args:
            crime_facts: The crime facts
            num_suspects: Number of suspects to generate

        Returns:
            List of suspect characters
        """
        prompt = f"""Generate {num_suspects} innocent suspects for this crime:

Crime type: {crime_facts.crime_type}
Victim: {crime_facts.victim.name} ({crime_facts.victim.occupation})
Setting: {crime_facts.location}

Each suspect should have:
1. A plausible motive (but they didn't do it)
2. Some connection to the victim
3. A real alibi (that might be hard to verify)

Format as JSON:
{{
    "suspects": [
        {{
            "name": "name",
            "occupation": "job",
            "relationship_to_victim": "how they knew victim",
            "apparent_motive": "why they might seem guilty",
            "alibi": "their real alibi"
        }}
    ]
}}"""

        response = self.llm.generate_with_retry(
            prompt=prompt,
            expect_json=True,
        )

        suspects = []
        if response.parsed_json and "suspects" in response.parsed_json:
            for s_data in response.parsed_json["suspects"]:
                suspect = Character(
                    name=s_data.get("name", f"Suspect_{len(suspects)}"),
                    role=CharacterRole.SUSPECT,
                    occupation=s_data.get("occupation", "Unknown"),
                    motive=s_data.get("apparent_motive", "Unknown"),
                    alibi=s_data.get("alibi", "Unknown"),
                    relationship_to_victim=s_data.get("relationship_to_victim", "Unknown"),
                )
                suspects.append(suspect)

        return suspects
