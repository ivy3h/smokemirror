"""
Prompt templates for the Smokemirror story generation system.
"""


class PromptTemplates:
    """Collection of prompt templates for different generation tasks."""

    # ========== Crime Backstory Generation ==========

    CRIME_BACKSTORY_SYSTEM = """You are a master crime fiction author specializing in crafting intricate mystery plots.
Your task is to create detailed, internally consistent crime backstories with complex conspirator networks.
Focus on creating realistic motivations, methods, and relationships between characters."""

    CRIME_BACKSTORY_PROMPT = """Create a detailed crime backstory for a mystery story. Generate a structured crime scenario.

Requirements:
1. Crime type: {crime_type}
2. Number of conspirators: {num_conspirators}
3. Setting: {setting}

Generate the following in valid JSON format:
{{
    "crime_type": "the type of crime",
    "victim": {{
        "name": "victim's name",
        "occupation": "their job",
        "relationship_to_criminal": "how they knew the criminal"
    }},
    "criminal": {{
        "name": "criminal's name",
        "occupation": "their job",
        "motive": "why they committed the crime",
        "means": "how they had the ability to commit it",
        "opportunity": "when/how they had the chance"
    }},
    "conspirators": [
        {{
            "name": "conspirator name",
            "occupation": "their job",
            "role_in_crime": "what they did to help",
            "leverage": "why they agreed to help (blackmail, debt, loyalty, etc.)",
            "alibi_provided": "what false alibi they provide"
        }}
    ],
    "method": "detailed description of how the crime was committed",
    "timeline": [
        {{"time": "time", "event": "what happened", "actor": "who did it", "location": "where"}}
    ],
    "evidence": [
        {{
            "id": "E1",
            "description": "what the evidence is",
            "type": "physical/testimonial/documentary/digital",
            "location": "where it was found/left",
            "real_meaning": "what it actually proves"
        }}
    ],
    "location": "main crime location",
    "coordination_plan": "how the conspirators coordinate their cover-up"
}}

Be creative and ensure all details are internally consistent. The crime should be complex enough to support at least 15 plot points in the investigation."""

    # ========== Fabricated Narrative Generation ==========

    FABRICATED_NARRATIVE_SYSTEM = """You are a criminal mastermind who must create a convincing false narrative to cover up a crime.
Your fabricated story must account for all physical evidence while pointing to an innocent person.
Think like a conspirator: what would make investigators believe your story?"""

    FABRICATED_NARRATIVE_PROMPT = """Given the following real crime facts, create a fabricated narrative that the conspirators will present to investigators.

REAL CRIME FACTS:
{real_facts}

Requirements:
1. Create a fake suspect who appears to have means, motive, and opportunity
2. The fabricated story must explain all physical evidence differently
3. Create false alibis for all conspirators
4. The story must be internally consistent
5. Include planted evidence to frame the fake suspect

Generate the fabricated narrative in valid JSON format:
{{
    "fake_suspect": {{
        "name": "name of innocent person to frame",
        "occupation": "their job",
        "fake_motive": "why they supposedly did it",
        "fake_means": "how they supposedly had ability",
        "fake_opportunity": "when/how they supposedly had chance",
        "background": "details making them a plausible suspect"
    }},
    "fake_timeline": [
        {{"time": "time", "event": "fabricated event", "actor": "who supposedly did it", "location": "where"}}
    ],
    "planted_evidence": [
        {{
            "id": "PE1",
            "description": "what was planted",
            "type": "evidence type",
            "location": "where it was planted",
            "fabricated_meaning": "what it supposedly proves"
        }}
    ],
    "alibis": {{
        "conspirator_name": "their alibi story"
    }},
    "cover_story": "the overall narrative the conspirators will tell",
    "evidence_explanations": {{
        "evidence_id": "how this real evidence fits the fabricated narrative"
    }}
}}

Make the fabricated narrative plausible enough to fool an experienced detective initially."""

    # ========== Detective Action Generation ==========

    DETECTIVE_ACTION_PROMPT = """You are writing the next action of a detective investigating a crime.

CURRENT CASE STATE:
- Crime: {crime_summary}
- What detective knows so far: {detective_knowledge}
- Current leads: {current_leads}
- Recent developments: {recent_developments}

Generate the detective's next investigative action. The action should:
1. Follow logically from what the detective currently knows
2. Attempt to verify or follow up on existing leads
3. Be a concrete, specific action (interview, examine evidence, visit location, etc.)

Format your response as:
{{
    "action": "specific action the detective takes",
    "reasoning": "why the detective chose this action",
    "target": "who/what is the target of this action",
    "expected_outcome": "what the detective hopes to learn"
}}"""

    # ========== Collision Detection ==========

    COLLISION_CHECK_PROMPT = """Analyze whether this detective action could expose the truth about the crime.

REAL CRIME FACTS (hidden from detective):
{real_facts}

FABRICATED NARRATIVE (what detective is meant to believe):
{fabricated_facts}

DETECTIVE'S ACTION:
{detective_action}

Analyze:
1. Does this action bring the detective close to discovering a discrepancy between the two narratives?
2. Which conspirator(s) would be most threatened by this action?
3. What specific crack in the fabricated narrative might be exposed?

Respond in JSON format:
{{
    "is_collision": true/false,
    "collision_severity": "none/minor/moderate/severe",
    "threatened_conspirators": ["names"],
    "vulnerable_point": "what could be exposed",
    "intervention_urgency": "none/low/medium/high"
}}"""

    # ========== Conspirator Intervention ==========

    CONSPIRATOR_INTERVENTION_PROMPT = """A conspirator must intervene to prevent the detective from discovering the truth.

SITUATION:
{situation}

CONSPIRATOR:
- Name: {conspirator_name}
- Role in crime: {conspirator_role}
- Available leverage/resources: {conspirator_resources}

VULNERABLE POINT:
{vulnerable_point}

Generate an intervention that:
1. Appears natural and not suspicious
2. Effectively patches the crack in the fabricated narrative
3. Is consistent with the conspirator's character and position
4. Closes off this path to the truth

Format your response as:
{{
    "intervention_type": "type of intervention (provide information, destroy evidence, redirect, etc.)",
    "action": "specific action the conspirator takes",
    "justification": "how they explain their involvement to the detective",
    "effectiveness": "how this closes off the discovery path",
    "risk_level": "low/medium/high - how suspicious might this appear"
}}"""

    # ========== Obstacle Generation ==========

    OBSTACLE_PROMPT = """Generate an obstacle that delays the detective's progress without involving conspirator intervention.

DETECTIVE'S ACTION:
{detective_action}

CURRENT STATE:
{current_state}

Generate a natural obstacle (bureaucratic delay, uncooperative witness, missing records, etc.) that:
1. Is realistic and not contrived
2. Delays but doesn't permanently block the investigation
3. Increases narrative tension

Format your response as:
{{
    "obstacle_type": "type of obstacle",
    "description": "what happens",
    "impact": "how this affects the investigation",
    "duration": "how long this delays things",
    "workaround": "potential way around this obstacle (for future plot points)"
}}"""

    # ========== Plot Point Assembly ==========

    PLOT_POINT_PROMPT = """Combine the following elements into a coherent plot point for the mystery story.

DETECTIVE ACTION: {detective_action}
OUTCOME: {outcome}
{intervention_or_obstacle}

Write this plot point as it would appear in the story. Include:
1. The detective's perspective and thoughts
2. What they observe and conclude
3. Dialogue if relevant
4. How this advances or complicates the investigation

The tone should be suspenseful. The reader knows the truth but watches the detective being misled.

Write the plot point (2-3 paragraphs):"""

    # ========== Reader Simulation ==========

    READER_LOGIC_ANALYST_PROMPT = """You are a Logic Analyst reader evaluating this mystery story.

STORY (detective's perspective only):
{story}

Analyze the story for:
1. Logical consistency of timelines and alibis
2. Whether the detective's reasoning follows from available evidence
3. Any inconsistencies in character statements
4. Attempt to deduce the real criminal based on the detective's information

For each plot point, rate suspense (1-10) and flag any logical issues.

At checkpoints (plot points {checkpoints}), provide your criminal prediction with reasoning.

Respond in JSON format:
{{
    "suspense_scores": {{"plot_point_id": score}},
    "criminal_predictions": {{
        "checkpoint_num": {{"prediction": "suspect name", "reasoning": "why", "confidence": "low/medium/high"}}
    }},
    "inconsistency_flags": [
        {{"plot_point": id, "issue": "description", "severity": "minor/moderate/critical"}}
    ],
    "engagement_assessment": {{
        "most_engaging": [plot_point_ids],
        "least_engaging": [plot_point_ids],
        "comments": "overall assessment"
    }},
    "overall_score": score_1_to_10
}}"""

    READER_INTUITIVE_PROMPT = """You are an Intuitive Reader evaluating this mystery story.

STORY (detective's perspective only):
{story}

Focus on:
1. Whether characters behave naturally and authentically
2. Whether dialogue feels genuine
3. Moments where something feels "too convenient"
4. Emotional authenticity of character reactions

For each plot point, rate suspense (1-10) and flag any immersion-breaking moments.

Respond in JSON format:
{{
    "suspense_scores": {{"plot_point_id": score}},
    "criminal_predictions": {{
        "checkpoint_num": {{"prediction": "suspect name", "reasoning": "why", "confidence": "low/medium/high"}}
    }},
    "inconsistency_flags": [
        {{"plot_point": id, "issue": "description", "severity": "minor/moderate/critical"}}
    ],
    "engagement_assessment": {{
        "most_engaging": [plot_point_ids],
        "least_engaging": [plot_point_ids],
        "comments": "overall assessment"
    }},
    "overall_score": score_1_to_10
}}"""

    READER_GENRE_EXPERT_PROMPT = """You are a Genre Expert reader (experienced in mystery fiction) evaluating this story.

STORY (detective's perspective only):
{story}

Focus on:
1. Pacing - does the story drag or rush at any point?
2. Trope usage - are any mystery clichés overused?
3. Red herring effectiveness - are misdirections too obvious or too subtle?
4. Narrative structure - does the story follow satisfying mystery conventions?

For each plot point, rate suspense (1-10) and provide genre-specific feedback.

Respond in JSON format:
{{
    "suspense_scores": {{"plot_point_id": score}},
    "criminal_predictions": {{
        "checkpoint_num": {{"prediction": "suspect name", "reasoning": "why", "confidence": "low/medium/high"}}
    }},
    "inconsistency_flags": [
        {{"plot_point": id, "issue": "description", "severity": "minor/moderate/critical"}}
    ],
    "engagement_assessment": {{
        "most_engaging": [plot_point_ids],
        "least_engaging": [plot_point_ids],
        "comments": "overall assessment"
    }},
    "pacing_analysis": {{
        "flat_sections": [plot_point_ranges],
        "rushed_sections": [plot_point_ranges],
        "well_paced_sections": [plot_point_ranges]
    }},
    "trope_analysis": {{
        "overused_tropes": ["list of tropes"],
        "effective_tropes": ["list of tropes"]
    }},
    "overall_score": score_1_to_10
}}"""

    # ========== Story Revision ==========

    REVISION_PROMPT = """Revise the following plot point(s) based on feedback.

ORIGINAL PLOT POINT(S):
{original_plot_points}

ISSUES IDENTIFIED:
{issues}

REVISION DIRECTIVE:
{revision_directive}

CONTEXT:
- Previous plot point: {previous_context}
- Following plot point: {following_context}

Rewrite the plot point(s) to address the issues while:
1. Maintaining consistency with surrounding plot points
2. Preserving the overall story direction
3. Improving suspense and engagement
4. Fixing any logical inconsistencies

Provide the revised plot point(s):"""

    # ========== Final Assembly ==========

    STORY_ASSEMBLY_PROMPT = """Assemble the following plot points into a cohesive, polished mystery narrative.

PLOT POINTS:
{plot_points}

REAL CRIME BACKGROUND (for reader revelations):
{real_crime_summary}

Create a final narrative that:
1. Flows smoothly between plot points
2. Interleaves detective perspective with reader-facing revelations about the conspiracy
3. Builds suspense progressively
4. Uses vivid, engaging prose
5. Maintains the dual-layer structure (reader knows truth, detective doesn't)

Format the story with clear section breaks. Use the reader's privileged knowledge to create dramatic irony.

Write the complete narrative:"""

    @classmethod
    def get_reader_prompt(cls, role: str) -> str:
        """Get the appropriate reader prompt based on role."""
        prompts = {
            "logic_analyst": cls.READER_LOGIC_ANALYST_PROMPT,
            "intuitive_reader": cls.READER_INTUITIVE_PROMPT,
            "genre_expert": cls.READER_GENRE_EXPERT_PROMPT,
        }
        return prompts.get(role, cls.READER_LOGIC_ANALYST_PROMPT)
