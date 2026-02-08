"""
Suspense Meta-Controller

The core generation component that iteratively generates the detective's
investigation story while managing suspense through discovery path management
and conspirator interventions.
"""

import json
import logging
import random
from typing import Optional

from ..models.llm_wrapper import LLMWrapper
from ..data_structures.facts import (
    CrimeFacts,
    FabricatedFacts,
    PlotPoint,
    DiscoveryPath,
    StoryState,
    DetectiveProfile,
)
from ..utils.prompts import PromptTemplates
from ..utils.config import SuspenseConfig, GenerationConfig

logger = logging.getLogger(__name__)


class CollisionDetector:
    """Non-neural module for detecting when detective approaches truth.

    Uses keyword extraction from pre-generated facts for semantic matching,
    rather than requiring exact string matches.
    """

    # Common words to exclude from keyword matching
    STOP_WORDS = frozenset({
        "the", "a", "an", "of", "in", "at", "on", "is", "was", "for", "to",
        "and", "or", "by", "it", "be", "as", "with", "from", "that", "this",
        "has", "had", "have", "not", "but", "are", "were", "been", "their",
    })

    def __init__(self, sensitivity: float = 0.5):
        self.sensitivity = sensitivity

    def _extract_keywords(self, text: str) -> set[str]:
        """Extract meaningful keywords from a text string."""
        words = set(text.lower().split())
        return {w for w in words if len(w) > 2 and w not in self.STOP_WORDS}

    def _name_matches(self, name: str, text: str) -> bool:
        """Check if a character name (or any part of it) appears in text."""
        text_lower = text.lower()
        name_lower = name.lower()
        # Full name match
        if name_lower in text_lower:
            return True
        # Any name part with 3+ chars matches
        for part in name_lower.split():
            if len(part) >= 3 and part in text_lower:
                return True
        return False

    def check_collision(
        self,
        detective_action: str,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
        open_paths: list[DiscoveryPath],
    ) -> tuple[bool, Optional[str], Optional[str]]:
        """Check if detective action could expose truth.

        Uses semantic keyword matching against pre-generated facts rather
        than requiring exact string matches.
        """
        action_lower = detective_action.lower()
        action_keywords = self._extract_keywords(detective_action)

        collision_detected = False
        vulnerable_point = None
        threatened_conspirator = None

        investigation_verbs = {
            "interview", "question", "alibi", "whereabouts", "talk",
            "ask", "confront", "investigate", "verify", "check", "examine",
        }

        # 1. Check if investigating a conspirator (partial name match)
        for conspirator in real_facts.conspirators:
            if self._name_matches(conspirator.name, action_lower):
                if action_keywords & investigation_verbs:
                    collision_detected = random.random() < self.sensitivity
                    if collision_detected:
                        vulnerable_point = (
                            f"Inconsistency in {conspirator.name}'s alibi"
                        )
                        threatened_conspirator = conspirator.name
                    break

        # 2. Check if examining evidence (keyword overlap with descriptions)
        if not collision_detected:
            for evidence in real_facts.evidence:
                if not (evidence.real_meaning and evidence.fabricated_meaning):
                    continue
                evidence_keywords = self._extract_keywords(evidence.description)
                overlap = action_keywords & evidence_keywords
                # 2+ keyword overlap = likely investigating this evidence
                if len(overlap) >= 2 or evidence.id.lower() in action_lower:
                    collision_detected = random.random() < self.sensitivity
                    if collision_detected:
                        vulnerable_point = (
                            f"True meaning of {evidence.description}"
                        )
                        # Find which conspirator this threatens
                        for c in real_facts.conspirators:
                            if self._name_matches(
                                c.name, evidence.real_meaning or ""
                            ):
                                threatened_conspirator = c.name
                                break
                        if not threatened_conspirator and real_facts.conspirators:
                            threatened_conspirator = real_facts.conspirators[0].name
                        break

        # 3. Check if visiting a crime-relevant location
        if not collision_detected:
            for event in real_facts.timeline.events:
                location = event.get("location", "")
                actor = event.get("actor", "")
                if location and location.lower() in action_lower:
                    collision_detected = random.random() < (self.sensitivity * 0.8)
                    if collision_detected:
                        vulnerable_point = (
                            f"Activity at {location} during the crime"
                        )
                        for c in real_facts.conspirators:
                            if self._name_matches(c.name, actor):
                                threatened_conspirator = c.name
                                break
                        if not threatened_conspirator and real_facts.conspirators:
                            threatened_conspirator = real_facts.conspirators[0].name
                        break

        # 4. Check discovery paths (keyword overlap instead of exact match)
        if not collision_detected:
            for path in open_paths:
                path_keywords = self._extract_keywords(path.description)
                if len(action_keywords & path_keywords) >= 2:
                    collision_detected = random.random() < (
                        self.sensitivity + 0.2
                    )
                    if collision_detected:
                        vulnerable_point = path.description
                        if path.involves_character:
                            threatened_conspirator = path.involves_character
                        break
                # Also check character name
                if (
                    path.involves_character
                    and self._name_matches(path.involves_character, action_lower)
                ):
                    collision_detected = random.random() < (
                        self.sensitivity + 0.1
                    )
                    if collision_detected:
                        vulnerable_point = path.description
                        threatened_conspirator = path.involves_character
                        break

        return collision_detected, vulnerable_point, threatened_conspirator


class SuspenseMetaController:
    """Controls the iterative generation of the detective story."""

    def __init__(
        self,
        llm: LLMWrapper,
        suspense_config: SuspenseConfig,
        generation_config: GenerationConfig,
    ):
        """Initialize the controller.

        Args:
            llm: LLM wrapper for generation
            suspense_config: Suspense-related configuration
            generation_config: General generation configuration
        """
        self.llm = llm
        self.suspense_config = suspense_config
        self.generation_config = generation_config
        self.collision_detector = CollisionDetector(
            sensitivity=suspense_config.collision_check_sensitivity
        )

    def generate_story(
        self,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
        discovery_paths: list[DiscoveryPath],
    ) -> tuple[list[PlotPoint], StoryState]:
        """Generate the complete detective investigation story.

        Args:
            real_facts: The real crime facts
            fabricated_facts: The fabricated narrative
            discovery_paths: Initial discovery paths

        Returns:
            Tuple of (list of PlotPoints, final StoryState)
        """
        logger.info("Starting suspense meta-controller generation")

        # Generate detective profile with personal stakes (elements a, b, c)
        detective_profile = self._generate_detective_profile(real_facts)
        logger.info(f"Detective: {detective_profile.name}")
        logger.info(f"Stakes: {detective_profile.personal_stakes}")
        logger.info(f"Dire consequence: {detective_profile.dire_consequence}")
        logger.info(f"Deadline: {detective_profile.deadline_reason}")

        # Initialize story state with countdown mechanism
        total_time = self.generation_config.max_plot_points + 3
        state = StoryState(
            reader_knowledge=self._initialize_reader_knowledge(real_facts),
            detective_knowledge=set(),
            discovery_paths=discovery_paths.copy(),
            suspense_level=self.suspense_config.initial_level,
            current_phase="investigation",
            detective_profile=detective_profile,
            time_remaining=total_time,
            total_time=total_time,
            success_probability=0.7,
            action_history=[],
            evidence_progress={e.id: 0 for e in real_facts.evidence},
            undiscovered_evidence=[e.id for e in real_facts.evidence],
            alibi_status={c.name: "unverified" for c in real_facts.conspirators},
        )

        plot_points = []
        iteration = 0
        max_iterations = self.generation_config.max_plot_points

        while iteration < max_iterations:
            iteration += 1
            state.time_remaining -= 1  # Countdown ticks
            logger.info(
                f"Generating plot point {iteration} | "
                f"Time: {state.time_remaining}/{state.total_time} | "
                f"Success prob: {state.success_probability:.0%}"
            )

            # Check termination: countdown expired
            if state.time_remaining <= 0:
                state.current_phase = "resolution"
                logger.info("TIME'S UP — forced resolution under deadline pressure")
                resolution_point = self._generate_resolution_point(
                    iteration, state, real_facts, fabricated_facts
                )
                plot_points.append(resolution_point)
                break

            # Check termination: discovery paths exhausted
            open_paths = state.get_open_paths()
            if len(open_paths) <= self.generation_config.discovery_paths_threshold:
                if len(plot_points) >= self.generation_config.min_plot_points:
                    state.current_phase = "resolution"
                    logger.info("Transitioning to resolution phase")
                    resolution_point = self._generate_resolution_point(
                        iteration, state, real_facts, fabricated_facts
                    )
                    plot_points.append(resolution_point)
                    break

            # Step 1: Generate detective action
            detective_action = self._generate_detective_action(
                state, real_facts, fabricated_facts
            )

            # Step 2: Check for layer collision
            is_collision, vulnerable_point, threatened_conspirator = (
                self.collision_detector.check_collision(
                    detective_action,
                    real_facts,
                    fabricated_facts,
                    open_paths,
                )
            )

            # Step 3: Generate outcome based on collision
            if is_collision and threatened_conspirator:
                # Generate conspirator intervention
                plot_point = self._generate_intervention_point(
                    iteration,
                    detective_action,
                    vulnerable_point,
                    threatened_conspirator,
                    state,
                    real_facts,
                    fabricated_facts,
                )
            else:
                # Generate standard obstacle or progress
                plot_point = self._generate_standard_point(
                    iteration,
                    detective_action,
                    state,
                    real_facts,
                    fabricated_facts,
                )

            # Step 4: Track action in accumulated history (for iterative context)
            action_record = {
                "action": detective_action,
                "outcome": plot_point.description,
                "was_blocked": is_collision,
                "blocked_by": plot_point.conspirator_intervention if is_collision else None,
                "obstacle": plot_point.obstacle,
                "detective_learned": plot_point.detective_learns,
            }
            state.action_history.append(action_record)

            # Step 5: Update state (countdown, probability, paths)
            self._update_state(state, plot_point, is_collision)

            plot_points.append(plot_point)
            state.plot_points.append(plot_point)

            logger.info(
                f"Plot point {iteration}: suspense={plot_point.suspense_level}, "
                f"success_prob={state.success_probability:.0%}, "
                f"time={state.time_remaining}/{state.total_time}, "
                f"open_paths={len(state.get_open_paths())}"
            )

        return plot_points, state

    def _initialize_reader_knowledge(self, real_facts: CrimeFacts) -> set:
        """Initialize what the reader knows at the start.

        Args:
            real_facts: Real crime facts

        Returns:
            Set of facts the reader knows
        """
        return {
            f"criminal:{real_facts.criminal.name}",
            f"motive:{real_facts.motive}",
            f"method:{real_facts.method}",
            f"conspirators:{','.join([c.name for c in real_facts.conspirators])}",
        }

    def _generate_detective_profile(self, real_facts: CrimeFacts) -> DetectiveProfile:
        """Generate a detective with personal stakes and a deadline.

        Implements suspense elements (a)-(c):
        (a) Reader affinity — a protagonist the reader cares about
        (b) Important objective — solving the case with personal meaning
        (c) Dire consequence — specific bad outcome if the detective fails
        """
        prompt = PromptTemplates.DETECTIVE_STAKES_PROMPT.format(
            crime_summary=(
                f"{real_facts.crime_type} involving {real_facts.victim.name} "
                f"({real_facts.victim.occupation}) at {real_facts.location}"
            ),
            setting=real_facts.location,
        )

        response = self.llm.generate_with_retry(
            prompt=prompt,
            expect_json=True,
        )

        if response.parsed_json:
            return DetectiveProfile(
                name=response.parsed_json.get("name", "Detective Morgan"),
                background=response.parsed_json.get(
                    "background", "Veteran homicide detective"
                ),
                personal_stakes=response.parsed_json.get(
                    "personal_stakes",
                    "Career on the line after a recent failure",
                ),
                dire_consequence=response.parsed_json.get(
                    "dire_consequence",
                    "Will be forced off the case and an innocent person convicted",
                ),
                deadline_reason=response.parsed_json.get(
                    "deadline_reason",
                    "Key evidence will be destroyed in 72 hours",
                ),
            )

        # Fallback
        return DetectiveProfile(
            name="Detective Morgan",
            background="Veteran detective with 15 years on the force",
            personal_stakes="This case mirrors an unsolved case that haunts them",
            dire_consequence="The real criminal escapes and the detective's career ends",
            deadline_reason="Key witness leaving the country in 72 hours",
        )

    def _format_action_history(self, action_history: list[dict]) -> str:
        """Format accumulated action history for prompt context.

        Implements the iterative accumulated context pattern from the PDF:
        each prompt sees ALL previous actions and their outcomes, so the LLM
        generates new actions that are distinct from everything tried before.
        """
        if not action_history:
            return "No actions taken yet. This is the start of the investigation."

        lines = []
        for i, record in enumerate(action_history, 1):
            line = f"Action {i}: {record['action']}"
            line += f"\n  -> Outcome: {record['outcome']}"
            if record.get("was_blocked") and record.get("blocked_by"):
                line += f"\n  -> [BLOCKED] {record['blocked_by']}"
            if record.get("obstacle"):
                line += f"\n  -> [OBSTACLE] {record['obstacle']}"
            if record.get("detective_learned"):
                line += f"\n  -> Detective learned: {record['detective_learned']}"
            lines.append(line)

        return "\n\n".join(lines)

    def _get_urgency_note(self, state: StoryState) -> str:
        """Generate an urgency note based on countdown status."""
        ratio = state.time_remaining / state.total_time if state.total_time > 0 else 0
        if ratio <= 0.15:
            return (
                "CRITICAL: Almost no time left! The detective is desperate "
                "and must act decisively or accept failure."
            )
        elif ratio <= 0.3:
            return (
                "URGENT: Time is running dangerously low. The detective feels "
                "the pressure mounting with every passing hour."
            )
        elif ratio <= 0.5:
            return (
                "The clock is ticking. The detective is increasingly aware "
                "that time is not on their side."
            )
        else:
            return "The investigation is underway. Time pressure is present but manageable for now."

    def _build_investigation_agenda(
        self,
        state: StoryState,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ) -> str:
        """Build a structured investigation agenda from pre-generated facts.

        This is the key mechanism for deeply integrating pre-generated crime
        details into the investigation process (Project Specific Question).
        It gives the LLM a concrete menu of evidence, suspects, and alibis
        to drive specific detective actions.
        """
        lines = []

        # Evidence items and their discovery progress
        lines.append("EVIDENCE TO INVESTIGATE:")
        for eid in state.undiscovered_evidence:
            evidence = next((e for e in real_facts.evidence if e.id == eid), None)
            if evidence:
                progress = state.evidence_progress.get(eid, 0)
                if progress > 0:
                    lines.append(
                        f"  - [{eid}] {evidence.description} at {evidence.location} "
                        f"[{progress}/{evidence.steps_required} steps done — needs more work]"
                    )
                else:
                    lines.append(
                        f"  - [{eid}] {evidence.description} at {evidence.location} "
                        f"[requires {evidence.steps_required} step(s)]"
                    )
        if not state.undiscovered_evidence:
            lines.append("  All known evidence has been examined.")

        # Alibis to verify
        lines.append("\nALIBIS TO VERIFY:")
        for name, status in state.alibi_status.items():
            conspirator = next(
                (c for c in real_facts.conspirators if c.name == name), None
            )
            if conspirator:
                alibi_desc = conspirator.alibi or "claims to have been elsewhere"
                lines.append(f"  - {name} ({conspirator.occupation}): \"{alibi_desc}\" [status: {status}]")

        # Known suspects
        lines.append("\nKNOWN SUSPECTS:")
        lines.append(
            f"  - Primary suspect: {fabricated_facts.fake_suspect.name} "
            f"({fabricated_facts.fake_suspect.occupation}) — "
            f"alleged motive: {fabricated_facts.fake_motive}"
        )
        lines.append(f"  - Real criminal (unknown to detective): conspirators are shielding the truth")

        # Crime scene
        lines.append(f"\nCRIME SCENE: {real_facts.location}")
        lines.append(f"CRIME TYPE: {real_facts.crime_type}")

        return "\n".join(lines)

    def _generate_detective_action(
        self,
        state: StoryState,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ) -> str:
        """Generate the detective's next investigative action.

        Uses FULL accumulated action history so each prompt references ALL
        previous attempts. Includes investigation agenda built from
        pre-generated crime facts.
        """
        detective_knowledge = (
            list(state.detective_knowledge) if state.detective_knowledge else ["Nothing yet"]
        )
        current_leads = [p.description for p in state.get_open_paths()]
        open_count = len(state.get_open_paths())
        total_count = len(state.discovery_paths)

        # Build full accumulated action history
        accumulated_actions = self._format_action_history(state.action_history)

        # Build investigation agenda from pre-generated facts
        investigation_agenda = self._build_investigation_agenda(
            state, real_facts, fabricated_facts
        )

        profile = state.detective_profile or DetectiveProfile(
            name="The Detective",
            background="",
            personal_stakes="Solve the case",
            dire_consequence="Failure",
            deadline_reason="Time is limited",
        )

        prompt = PromptTemplates.DETECTIVE_ACTION_PROMPT.format(
            crime_summary=(
                f"{real_facts.crime_type} - victim: {real_facts.victim.name} "
                f"({real_facts.victim.occupation}) at {real_facts.location}"
            ),
            detective_name=profile.name,
            detective_stakes=profile.personal_stakes,
            dire_consequence=profile.dire_consequence,
            time_remaining=state.time_remaining,
            total_time=state.total_time,
            deadline_reason=profile.deadline_reason,
            success_probability=f"{state.success_probability * 100:.0f}",
            accumulated_actions=accumulated_actions,
            investigation_agenda=investigation_agenda,
            detective_knowledge="; ".join(str(k) for k in detective_knowledge),
            current_leads=(
                "; ".join(current_leads) if current_leads
                else "No clear leads remaining"
            ),
            closed_paths_count=total_count - open_count,
            total_paths_count=total_count,
            num_previous_actions=len(state.action_history),
            urgency_note=self._get_urgency_note(state),
        )

        response = self.llm.generate_with_retry(
            prompt=prompt,
            expect_json=True,
        )

        if response.parsed_json and "action" in response.parsed_json:
            return response.parsed_json["action"]

        return response.text.split("\n")[0] if response.text else "Continue investigation"

    def _generate_intervention_point(
        self,
        plot_id: int,
        detective_action: str,
        vulnerable_point: str,
        threatened_conspirator: str,
        state: StoryState,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ) -> PlotPoint:
        """Generate a plot point with conspirator intervention.

        Args:
            plot_id: Plot point ID
            detective_action: What the detective did
            vulnerable_point: What could be exposed
            threatened_conspirator: Which conspirator is threatened
            state: Current story state
            real_facts: Real crime facts
            fabricated_facts: Fabricated narrative

        Returns:
            PlotPoint with intervention
        """
        # Find the conspirator
        conspirator = next(
            (c for c in real_facts.conspirators if c.name == threatened_conspirator),
            real_facts.conspirators[0] if real_facts.conspirators else None,
        )

        if conspirator is None:
            # Fallback if no conspirator found
            return self._generate_standard_point(
                plot_id, detective_action, state, real_facts, fabricated_facts
            )

        situation = f"""
The detective is {detective_action}.
This threatens to expose: {vulnerable_point}.
If the detective continues, they might discover the truth about the crime.
"""

        prompt = PromptTemplates.CONSPIRATOR_INTERVENTION_PROMPT.format(
            situation=situation,
            conspirator_name=conspirator.name,
            conspirator_role=conspirator.occupation,
            conspirator_resources=conspirator.leverage or "position of trust",
            vulnerable_point=vulnerable_point,
            time_remaining=state.time_remaining,
            total_time=state.total_time,
        )

        response = self.llm.generate_with_retry(
            prompt=prompt,
            expect_json=True,
        )

        intervention_text = "intervenes to misdirect"
        effectiveness = "redirects detective away from truth"

        if response.parsed_json:
            intervention_text = response.parsed_json.get("action", intervention_text)
            effectiveness = response.parsed_json.get("effectiveness", effectiveness)

        # Find and mark path as closed
        path_to_close = None
        for path in state.discovery_paths:
            if path.is_open and (
                path.involves_character == threatened_conspirator
                or vulnerable_point.lower() in path.description.lower()
            ):
                path_to_close = path.id
                break

        # Interventions increase suspense AND decrease success probability
        # This implements element (d): events making achieving objective less likely
        new_suspense = min(
            state.suspense_level + random.randint(1, 2),
            self.suspense_config.max_level,
        )
        state.success_probability = max(
            0.05, state.success_probability - random.uniform(0.06, 0.12)
        )

        return PlotPoint(
            id=plot_id,
            description=f"Detective {detective_action} but {conspirator.name} {intervention_text}",
            detective_action=detective_action,
            conspirator_intervention=f"{conspirator.name}: {intervention_text}",
            reader_revelation=f"The reader sees {conspirator.name} actively protecting the conspiracy",
            detective_learns=f"Detective accepts {conspirator.name}'s explanation",
            paths_closed=[path_to_close] if path_to_close else [],
            suspense_level=new_suspense,
            is_collision=True,
        )

    def _generate_standard_point(
        self,
        plot_id: int,
        detective_action: str,
        state: StoryState,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ) -> PlotPoint:
        """Generate a standard plot point using pre-generated crime details.

        Deeply integrates pre-generated facts: picks specific evidence items,
        tracks multi-step clue progress, and handles alibi verification.
        """
        has_obstacle = random.random() < 0.4

        obstacle_text = None
        detective_learns = None
        reader_revelation = None
        path_to_close = None

        if has_obstacle:
            prompt = PromptTemplates.OBSTACLE_PROMPT.format(
                detective_action=detective_action,
                current_state=f"Investigation of {fabricated_facts.fake_suspect.name}",
                time_remaining=state.time_remaining,
                total_time=state.total_time,
            )

            response = self.llm.generate_with_retry(
                prompt=prompt,
                expect_json=True,
            )

            if response.parsed_json:
                obstacle_text = response.parsed_json.get("description", "encounters a delay")

            description = f"Detective {detective_action} but {obstacle_text or 'encounters resistance'}"
            new_suspense = state.suspense_level
            state.success_probability = max(
                0.05, state.success_probability - random.uniform(0.02, 0.05)
            )

        else:
            # Pick a SPECIFIC progress type based on pre-generated facts
            progress_type = self._pick_progress_type(state, real_facts)

            if progress_type == "evidence":
                description, detective_learns, reader_revelation = (
                    self._progress_evidence_discovery(
                        detective_action, state, real_facts, fabricated_facts
                    )
                )
            elif progress_type == "alibi":
                description, detective_learns, reader_revelation = (
                    self._progress_alibi_check(
                        detective_action, state, real_facts
                    )
                )
            else:
                detective_learns = (
                    f"Evidence pointing toward {fabricated_facts.fake_suspect.name}"
                )
                description = (
                    f"Detective {detective_action} and finds {detective_learns}"
                )

            # Close a random path occasionally
            if random.random() < self.suspense_config.path_close_probability:
                open_paths = state.get_open_paths()
                if open_paths:
                    path_to_close = random.choice(open_paths).id

            # Progress gives a brief glimmer of hope
            state.success_probability = min(
                0.8, state.success_probability + random.uniform(0.01, 0.03)
            )
            new_suspense = min(
                state.suspense_level + random.randint(0, 1),
                self.suspense_config.max_level,
            )

        return PlotPoint(
            id=plot_id,
            description=description,
            detective_action=detective_action,
            obstacle=obstacle_text,
            reader_revelation=reader_revelation,
            detective_learns=detective_learns,
            paths_closed=[path_to_close] if path_to_close else [],
            suspense_level=new_suspense,
            is_collision=False,
        )

    def _pick_progress_type(
        self, state: StoryState, real_facts: CrimeFacts
    ) -> str:
        """Decide what type of progress the detective makes, weighted by
        what pre-generated facts are still available to investigate."""
        options = []
        if state.undiscovered_evidence:
            options.extend(["evidence"] * 3)
        if any(v == "unverified" for v in state.alibi_status.values()):
            options.extend(["alibi"] * 2)
        options.append("generic")
        return random.choice(options)

    def _progress_evidence_discovery(
        self,
        detective_action: str,
        state: StoryState,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ) -> tuple[str, str, Optional[str]]:
        """Handle evidence discovery with multi-step clue tracking.

        Returns: (description, detective_learns, reader_revelation)
        """
        # Prefer evidence that already has partial progress
        in_progress = [
            eid for eid in state.undiscovered_evidence
            if state.evidence_progress.get(eid, 0) > 0
        ]
        pick_from = in_progress if in_progress else state.undiscovered_evidence

        if not pick_from:
            return (
                f"Detective {detective_action} and finds corroborating details",
                f"Evidence pointing toward {fabricated_facts.fake_suspect.name}",
                None,
            )

        eid = random.choice(pick_from)
        evidence = next((e for e in real_facts.evidence if e.id == eid), None)
        if not evidence:
            return (
                f"Detective {detective_action} and finds corroborating details",
                f"Evidence pointing toward {fabricated_facts.fake_suspect.name}",
                None,
            )

        # Advance progress
        state.evidence_progress[eid] = state.evidence_progress.get(eid, 0) + 1
        steps_done = state.evidence_progress[eid]

        if steps_done >= evidence.steps_required:
            # Fully discovered — detective sees fabricated meaning
            if eid in state.undiscovered_evidence:
                state.undiscovered_evidence.remove(eid)
            fab_meaning = (
                evidence.fabricated_meaning
                or f"evidence implicating {fabricated_facts.fake_suspect.name}"
            )
            detective_learns = (
                f"Fully obtained {evidence.description} at {evidence.location}: "
                f"{fab_meaning}"
            )
            reader_revelation = (
                f"Reader knows the true meaning: {evidence.real_meaning}"
            )
            description = (
                f"Detective {detective_action} and fully obtains "
                f"{evidence.description} ({evidence.steps_required} steps complete)"
            )
        else:
            # Partial progress — multi-step clue not yet complete
            detective_learns = (
                f"Partial progress on {evidence.description} "
                f"({steps_done}/{evidence.steps_required} steps)"
            )
            reader_revelation = (
                f"Reader knows this evidence has deeper significance "
                f"the detective hasn't uncovered yet"
            )
            description = (
                f"Detective {detective_action} and makes partial progress "
                f"examining {evidence.description} "
                f"({steps_done}/{evidence.steps_required})"
            )

        return description, detective_learns, reader_revelation

    def _progress_alibi_check(
        self,
        detective_action: str,
        state: StoryState,
        real_facts: CrimeFacts,
    ) -> tuple[str, str, Optional[str]]:
        """Handle alibi verification for conspirators.

        Returns: (description, detective_learns, reader_revelation)
        """
        unverified = [
            name for name, status in state.alibi_status.items()
            if status == "unverified"
        ]
        if not unverified:
            return (
                f"Detective {detective_action} and reviews case notes",
                "All alibis have been checked",
                None,
            )

        char_name = random.choice(unverified)
        conspirator = next(
            (c for c in real_facts.conspirators if c.name == char_name), None
        )
        if not conspirator:
            return (
                f"Detective {detective_action} and reviews case notes",
                "Reviewed existing evidence",
                None,
            )

        state.alibi_status[char_name] = "challenged"
        alibi_text = conspirator.alibi or "claims to have been elsewhere"
        detective_learns = (
            f"Checked {char_name}'s alibi: \"{alibi_text}\" — "
            f"appears consistent on the surface"
        )
        reader_revelation = (
            f"Reader knows {char_name}'s alibi is fabricated — "
            f"they were actually involved in the crime"
        )
        description = (
            f"Detective {detective_action} and verifies "
            f"{char_name}'s alibi"
        )

        return description, detective_learns, reader_revelation

    def _generate_resolution_point(
        self,
        plot_id: int,
        state: StoryState,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ) -> PlotPoint:
        """Generate the resolution plot point.

        Args:
            plot_id: Plot point ID
            state: Current story state
            real_facts: Real crime facts
            fabricated_facts: Fabricated narrative

        Returns:
            Resolution PlotPoint
        """
        profile = state.detective_profile
        profile_info = ""
        if profile:
            profile_info = (
                f"\nDetective {profile.name} has been driven by: {profile.personal_stakes}"
                f"\nWhat's at stake: {profile.dire_consequence}"
                f"\nTime remaining: {state.time_remaining} of {state.total_time} units"
                f"\nEstimated success chance: {state.success_probability:.0%}"
            )

        # The detective either solves it (wrong) or misses the truth
        prompt = f"""Generate a resolution for this mystery:

The detective has been investigating {real_facts.crime_type}.
The REAL criminal is {real_facts.criminal.name}, but the detective has been
misled by conspirators to suspect {fabricated_facts.fake_suspect.name}.
{profile_info}

The detective tried {len(state.action_history)} different approaches but the
conspiracy held. Most discovery paths to the truth have been closed.

The detective must now make a conclusion. Options:
1. Detective arrests the wrong person (fabricated suspect) — the dire consequence unfolds
2. Detective senses something is wrong but can't prove it — haunted by the failure
3. Detective finds one last clue that reopens the case — a sliver of hope

Choose option 1 or 2 for a suspenseful ending where the conspiracy succeeds
and the detective faces the consequences of failure.
Write the resolution scene:"""

        response = self.llm.generate(prompt, max_new_tokens=512)

        return PlotPoint(
            id=plot_id,
            description="The investigation reaches its conclusion",
            detective_action="Reviews all evidence and makes final determination",
            reader_revelation=f"The reader watches as the truth remains hidden, {real_facts.criminal.name}'s secret safe",
            detective_learns=f"Concludes {fabricated_facts.fake_suspect.name} is the primary suspect",
            suspense_level=self.suspense_config.max_level,
            is_collision=False,
        )

    def _update_state(
        self,
        state: StoryState,
        plot_point: PlotPoint,
        is_collision: bool,
    ):
        """Update story state after generating a plot point.

        Manages suspense level, discovery paths, countdown, and success
        probability. Implements element (d): each turn makes success less likely.
        """
        # Update suspense level
        state.suspense_level = plot_point.suspense_level

        # Close paths — each closed path further reduces success probability
        for path_id in plot_point.paths_closed:
            state.close_path(path_id, f"plot_point_{plot_point.id}")
            state.success_probability = max(
                0.05, state.success_probability - random.uniform(0.03, 0.07)
            )

        # Update detective knowledge
        if plot_point.detective_learns:
            state.detective_knowledge.add(plot_point.detective_learns)

        # Time decay: success probability naturally decreases as time passes
        state.success_probability = max(
            0.05, state.success_probability - 0.01
        )

        # Occasionally open new minor path (for pacing — brief hope)
        if random.random() < self.suspense_config.new_path_probability:
            new_path = DiscoveryPath(
                id=f"path_new_{len(state.discovery_paths)}",
                description="A new potential lead emerges",
                difficulty=random.randint(6, 9),
            )
            state.discovery_paths.append(new_path)
            # New path gives slight hope
            state.success_probability = min(
                0.8, state.success_probability + 0.02
            )

    def revise_plot_points(
        self,
        plot_points: list[PlotPoint],
        revision_targets: list[int],
        revision_directives: list[dict],
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ) -> list[PlotPoint]:
        """Revise specific plot points based on feedback.

        Args:
            plot_points: Current plot points
            revision_targets: IDs of plot points to revise
            revision_directives: What to fix
            real_facts: Real crime facts
            fabricated_facts: Fabricated narrative

        Returns:
            Updated list of plot points
        """
        revised_points = plot_points.copy()

        for target_id in revision_targets:
            if target_id < 0 or target_id >= len(revised_points):
                continue

            original = revised_points[target_id]
            directives = [d for d in revision_directives if target_id in d.get("target_plot_points", [])]

            if not directives:
                continue

            # Get context
            prev_context = revised_points[target_id - 1].description if target_id > 0 else "Start of investigation"
            next_context = revised_points[target_id + 1].description if target_id < len(revised_points) - 1 else "End of story"

            prompt = PromptTemplates.REVISION_PROMPT.format(
                original_plot_points=json.dumps(original.to_dict()),
                issues=json.dumps([d.get("description", "") for d in directives]),
                revision_directive=json.dumps([d.get("suggested_revision", "") for d in directives]),
                previous_context=prev_context,
                following_context=next_context,
            )

            response = self.llm.generate(prompt, max_new_tokens=512)

            # Update the plot point
            revised_points[target_id] = PlotPoint(
                id=original.id,
                description=response.text[:200] if response.text else original.description,
                detective_action=original.detective_action,
                conspirator_intervention=original.conspirator_intervention,
                obstacle=original.obstacle,
                reader_revelation=original.reader_revelation,
                detective_learns=original.detective_learns,
                paths_closed=original.paths_closed,
                suspense_level=original.suspense_level + 1,  # Revision should improve suspense
                is_collision=original.is_collision,
            )

        return revised_points
