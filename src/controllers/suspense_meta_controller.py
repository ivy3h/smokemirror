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
)
from ..utils.prompts import PromptTemplates
from ..utils.config import SuspenseConfig, GenerationConfig

logger = logging.getLogger(__name__)


class CollisionDetector:
    """Non-neural module for detecting when detective approaches truth."""

    def __init__(self, sensitivity: float = 0.5):
        """Initialize detector.

        Args:
            sensitivity: How sensitive to potential collisions (0-1)
        """
        self.sensitivity = sensitivity

    def check_collision(
        self,
        detective_action: str,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
        open_paths: list[DiscoveryPath],
    ) -> tuple[bool, Optional[str], Optional[str]]:
        """Check if detective action could expose truth.

        Args:
            detective_action: What the detective is doing
            real_facts: Real crime facts
            fabricated_facts: Fabricated narrative
            open_paths: Currently open discovery paths

        Returns:
            Tuple of (is_collision, vulnerable_point, threatened_conspirator)
        """
        action_lower = detective_action.lower()

        # Check keywords that indicate approaching truth
        collision_keywords = {
            "security": ["footage", "camera", "log", "record"],
            "alibi": ["verify", "check", "confirm", "alibi"],
            "witness": ["witness", "saw", "seen", "observed"],
            "timeline": ["time", "when", "timeline", "schedule"],
            "motive": ["why", "motive", "reason", "benefit"],
            "evidence": ["evidence", "fingerprint", "dna", "trace"],
        }

        collision_detected = False
        vulnerable_point = None
        threatened_conspirator = None

        # Check for conspirator-related queries
        for conspirator in real_facts.conspirators:
            if conspirator.name.lower() in action_lower:
                # Detective is investigating a conspirator
                if any(keyword in action_lower for keyword in ["interview", "question", "alibi", "whereabouts"]):
                    collision_detected = random.random() < self.sensitivity
                    if collision_detected:
                        vulnerable_point = f"Inconsistency in {conspirator.name}'s alibi"
                        threatened_conspirator = conspirator.name
                    break

        # Check for evidence examination that could reveal truth
        for evidence in real_facts.evidence:
            if evidence.description.lower() in action_lower or evidence.id.lower() in action_lower:
                if evidence.real_meaning and evidence.fabricated_meaning:
                    collision_detected = random.random() < self.sensitivity
                    if collision_detected:
                        vulnerable_point = f"True meaning of {evidence.description}"
                        break

        # Check discovery paths
        for path in open_paths:
            if path.description.lower() in action_lower or (
                path.involves_character and path.involves_character.lower() in action_lower
            ):
                collision_detected = random.random() < (self.sensitivity + 0.2)
                if collision_detected:
                    vulnerable_point = path.description
                    if path.involves_character:
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

        # Initialize story state
        state = StoryState(
            reader_knowledge=self._initialize_reader_knowledge(real_facts),
            detective_knowledge=set(),
            discovery_paths=discovery_paths.copy(),
            suspense_level=self.suspense_config.initial_level,
            current_phase="investigation",
        )

        plot_points = []
        iteration = 0
        max_iterations = self.generation_config.max_plot_points

        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Generating plot point {iteration}")

            # Check termination condition
            open_paths = state.get_open_paths()
            if len(open_paths) <= self.generation_config.discovery_paths_threshold:
                if len(plot_points) >= self.generation_config.min_plot_points:
                    state.current_phase = "resolution"
                    logger.info("Transitioning to resolution phase")
                    # Generate final resolution plot point
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
                    fabricated_facts,
                )

            # Step 4: Update state
            self._update_state(state, plot_point, is_collision)

            plot_points.append(plot_point)
            state.plot_points.append(plot_point)

            logger.info(
                f"Plot point {iteration}: suspense={plot_point.suspense_level}, "
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

    def _generate_detective_action(
        self,
        state: StoryState,
        real_facts: CrimeFacts,
        fabricated_facts: FabricatedFacts,
    ) -> str:
        """Generate the detective's next investigative action.

        Args:
            state: Current story state
            real_facts: Real crime facts
            fabricated_facts: Fabricated narrative

        Returns:
            Description of detective's action
        """
        # Summarize current state for prompt
        detective_knowledge = list(state.detective_knowledge)[-5:] if state.detective_knowledge else ["Nothing yet"]
        current_leads = [p.description for p in state.get_open_paths()[:3]]
        recent = [pp.description for pp in state.plot_points[-2:]] if state.plot_points else ["Investigation just started"]

        prompt = PromptTemplates.DETECTIVE_ACTION_PROMPT.format(
            crime_summary=f"{real_facts.crime_type} - victim: {real_facts.victim.name}",
            detective_knowledge="; ".join(str(k) for k in detective_knowledge),
            current_leads="; ".join(current_leads) if current_leads else "Following general investigation procedures",
            recent_developments="; ".join(recent),
        )

        response = self.llm.generate_with_retry(
            prompt=prompt,
            expect_json=True,
        )

        if response.parsed_json and "action" in response.parsed_json:
            return response.parsed_json["action"]

        # Fallback to text extraction
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
                plot_id, detective_action, state, fabricated_facts
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

        # Calculate suspense level (interventions increase suspense)
        new_suspense = min(
            state.suspense_level + random.randint(1, 2),
            self.suspense_config.max_level,
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
        fabricated_facts: FabricatedFacts,
    ) -> PlotPoint:
        """Generate a standard plot point without intervention.

        Args:
            plot_id: Plot point ID
            detective_action: What the detective did
            state: Current story state
            fabricated_facts: Fabricated narrative

        Returns:
            PlotPoint with obstacle or progress
        """
        # Decide: obstacle or progress?
        has_obstacle = random.random() < 0.4  # 40% chance of obstacle

        obstacle_text = None
        detective_learns = None
        path_to_close = None

        if has_obstacle:
            prompt = PromptTemplates.OBSTACLE_PROMPT.format(
                detective_action=detective_action,
                current_state=f"Investigation of {fabricated_facts.fake_suspect.name}",
            )

            response = self.llm.generate_with_retry(
                prompt=prompt,
                expect_json=True,
            )

            if response.parsed_json:
                obstacle_text = response.parsed_json.get("description", "encounters a delay")

            description = f"Detective {detective_action} but {obstacle_text or 'encounters resistance'}"
            new_suspense = state.suspense_level  # Obstacles maintain suspense

        else:
            # Detective makes progress (within fabricated narrative)
            detective_learns = f"Evidence pointing toward {fabricated_facts.fake_suspect.name}"
            description = f"Detective {detective_action} and finds {detective_learns}"

            # Close a random path occasionally
            path_to_close = None
            if random.random() < self.suspense_config.path_close_probability:
                open_paths = state.get_open_paths()
                if open_paths:
                    path_to_close = random.choice(open_paths).id

            new_suspense = min(
                state.suspense_level + random.randint(0, 1),
                self.suspense_config.max_level,
            )

        return PlotPoint(
            id=plot_id,
            description=description,
            detective_action=detective_action,
            obstacle=obstacle_text,
            detective_learns=detective_learns,
            paths_closed=[path_to_close] if path_to_close else [],
            suspense_level=new_suspense,
            is_collision=False,
        )

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
        # The detective either solves it (wrong) or misses the truth
        prompt = f"""Generate a resolution for this mystery:

The detective has been investigating {real_facts.crime_type}.
The REAL criminal is {real_facts.criminal.name}, but the detective has been
misled by conspirators to suspect {fabricated_facts.fake_suspect.name}.

Most discovery paths to the truth have been closed. The detective must now
make a conclusion. Options:
1. Detective arrests the wrong person (fabricated suspect)
2. Detective senses something is wrong but can't prove it
3. Detective finds one last clue that reopens the case

Choose option 1 or 2 for a suspenseful ending where the conspiracy succeeds.
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

        Args:
            state: Story state to update
            plot_point: Generated plot point
            is_collision: Whether this was a collision point
        """
        # Update suspense level
        state.suspense_level = plot_point.suspense_level

        # Close paths
        for path_id in plot_point.paths_closed:
            state.close_path(path_id, f"plot_point_{plot_point.id}")

        # Update detective knowledge
        if plot_point.detective_learns:
            state.detective_knowledge.add(plot_point.detective_learns)

        # Occasionally open new minor path (for pacing)
        if random.random() < self.suspense_config.new_path_probability:
            new_path = DiscoveryPath(
                id=f"path_new_{len(state.discovery_paths)}",
                description="A new potential lead emerges",
                difficulty=random.randint(6, 9),
            )
            state.discovery_paths.append(new_path)

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
