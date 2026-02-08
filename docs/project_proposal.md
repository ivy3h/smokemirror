# Project Proposal: SmokeMirror

## Dual-Layer Narrative Generation with Suspense-Aware Plot Control for Mystery Fiction

---

## 1. Introduction & Motivation

### 1.1 Problem Statement

Large Language Models (LLMs) have demonstrated remarkable capabilities in creative text generation. However, generating **long-form mystery fiction** with sophisticated narrative structures remains a significant challenge. Specifically, mystery novels require:

1. **Dual-layer narrative structure**: The reader knows the truth (who committed the crime), while the detective character operates under false assumptions—creating sustained dramatic irony.

2. **Conspiracy and misdirection**: Multiple conspirators must coordinate to mislead the investigation while maintaining internal consistency.

3. **Suspense management**: The story must maintain tension through near-discoveries, strategic interventions, and carefully paced revelations.

4. **Long-range coherence**: Plot elements introduced early must remain consistent and pay off across tens of thousands of words.

Current LLM-based story generation systems struggle with these requirements because they lack:
- Explicit mechanisms for managing dual perspectives (reader vs. character knowledge)
- Structured approaches to suspense curve optimization
- Multi-agent coordination for conspiracy dynamics

### 1.2 Research Questions

1. **RQ1**: How can we design a generation framework that maintains separate knowledge states for readers and characters throughout a long narrative?

2. **RQ2**: Can we develop a "collision detection" mechanism that identifies when plot events threaten narrative consistency and triggers appropriate interventions?

3. **RQ3**: How do different reader perspectives (logical, intuitive, genre-aware) evaluate suspense quality, and can this feedback improve generation?

---

## 2. Proposed Approach: SmokeMirror

We propose **SmokeMirror**, a multi-phase pipeline for generating dual-layer mystery narratives with explicit suspense control.

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SmokeMirror Pipeline                      │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: World Building                                     │
│  ├── Crime Backstory Generator → Real Facts (Ground Truth)  │
│  ├── Discovery Paths → Routes to Truth                       │
│  └── Fabricated Narrative Generator → Cover Story           │
├─────────────────────────────────────────────────────────────┤
│  Phase 2: Suspense Meta-Controller                           │
│  ├── Detective Action Generation                             │
│  ├── Collision Detector (Truth Exposure Risk)               │
│  ├── Conspirator Intervention (Misdirection)                │
│  └── Discovery Path Management                               │
├─────────────────────────────────────────────────────────────┤
│  Phase 3: Story Assembly                                     │
│  ├── Dual-Layer Narrative Weaving                           │
│  └── Reader Layer (Truth) + Detective Layer (Illusion)      │
├─────────────────────────────────────────────────────────────┤
│  Phase 4: Reader Simulation & Evaluation                     │
│  ├── Logic Analyst (Deduction Quality)                      │
│  ├── Intuitive Reader (Emotional Engagement)                │
│  └── Genre Expert (Pacing & Structure)                      │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Key Technical Innovations

#### 2.2.1 Dual-Layer Fact Management

We maintain two parallel knowledge structures:
- **Real Facts**: The ground truth known to the reader (criminal identity, true motive, actual evidence meanings)
- **Fabricated Facts**: The false narrative constructed by conspirators (fake suspect, planted evidence, cover story)

The system ensures that detective actions only access fabricated facts while reader revelations expose the truth.

#### 2.2.2 Collision Detection Mechanism

At each plot point generation step, we check whether the detective's investigation threatens to expose the truth:

```python
def check_collision(detective_action, real_facts, open_discovery_paths):
    # Check if action investigates a conspirator
    # Check if action examines revealing evidence
    # Check if action follows a discovery path to truth
    → Returns: (is_collision, vulnerable_point, threatened_conspirator)
```

When collision is detected, the system triggers a **conspirator intervention** that:
- Misdirects the detective's attention
- Provides false but plausible explanations
- Closes the threatening discovery path

#### 2.2.3 Discovery Path Management

We model the detective's potential routes to truth as **discovery paths**:
- Each path represents a chain of evidence/witnesses leading to the real criminal
- Paths can be **opened** (new leads emerge) or **closed** (conspirators intervene)
- Story terminates when paths ≤ threshold (mystery remains unsolved) or detective finds truth

#### 2.2.4 Suspense Curve Optimization

We track suspense levels throughout the narrative:
- **Collision events** increase suspense (near-discoveries create tension)
- **Successful interventions** maintain suspense while adding dramatic irony
- **Path closures** reduce future discovery options, raising stakes

### 2.3 Reader Simulation

We employ three simulated reader perspectives to evaluate generated stories:

| Reader Type | Focus | Evaluation Criteria |
|-------------|-------|---------------------|
| Logic Analyst | Deduction | Are clues consistent? Can the mystery be solved fairly? |
| Intuitive Reader | Engagement | Are characters believable? Is the emotional arc satisfying? |
| Genre Expert | Structure | Does pacing follow mystery conventions? Is the climax earned? |

Each reader provides:
- Suspense scores per plot point
- Criminal predictions at checkpoints
- Inconsistency flags
- Engagement assessment

---

## 3. Experimental Design

### 3.1 Research Hypotheses

- **H1**: SmokeMirror generates stories with higher reader-perceived suspense than baseline LLM generation.
- **H2**: The collision detection mechanism produces more dramatic near-miss moments.
- **H3**: Dual-layer narratives create measurable dramatic irony that enhances engagement.
- **H4**: Multi-perspective reader simulation correlates with human evaluation.

### 3.2 Baselines

1. **Vanilla LLM**: Direct prompting of Qwen3-32B for mystery story generation
2. **Outline-then-Generate**: Two-stage generation with explicit plot outline
3. **Recursive Summarization**: Hierarchical generation with summary context
4. **Plan-and-Write**: Goal-directed story generation with explicit planning

### 3.3 Evaluation Metrics

#### Automatic Metrics
| Metric | Description |
|--------|-------------|
| Suspense Curve | Average suspense score, variance, trend (ascending/flat/descending) |
| Collision Rate | Frequency of near-discovery events |
| Path Close Rate | How effectively conspirators close discovery routes |
| Layer Leak Detection | Whether readers correctly identify the criminal early |
| Consistency Score | Logical coherence across the narrative |

#### Human Evaluation
- Suspense rating (1-10)
- Engagement rating (1-10)
- Dramatic irony recognition
- Willingness to continue reading
- Overall quality ranking

### 3.4 Dataset

We will generate and evaluate:
- **50 stories** using SmokeMirror (various crime types, settings, conspiracy sizes)
- **50 stories** per baseline method
- **Human evaluation** on a subset of 20 stories per method

---

## 4. Expected Contributions

1. **Novel Framework**: First system explicitly designed for dual-layer mystery narrative generation with reader/character knowledge separation.

2. **Collision Detection**: A new mechanism for identifying and managing narrative tension points where plot consistency is at risk.

3. **Suspense Modeling**: Quantitative approach to measuring and optimizing suspense curves in generated fiction.

4. **Multi-Perspective Evaluation**: Reader simulation framework that captures different aspects of mystery story quality.

5. **Benchmark & Dataset**: Generated mystery corpus with annotations for suspense, consistency, and dual-layer structure.

---

## 5. Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Phase 1 | Weeks 1-3 | System implementation, baseline setup |
| Phase 2 | Weeks 4-6 | Story generation, automatic evaluation |
| Phase 3 | Weeks 7-8 | Human evaluation study |
| Phase 4 | Weeks 9-10 | Analysis, paper writing |

---

## 6. Resources Required

### Computational
- 4× NVIDIA A40 GPUs (for Qwen3-32B inference)
- 1× NVIDIA A40 GPU (for reader model evaluation)
- Estimated: 200+ GPU hours for full experiments

### Human Evaluation
- 20-30 participants for story evaluation
- IRB approval for human subjects research

---

## 7. Broader Impact

### Positive Applications
- **Creative writing assistance**: Help authors develop complex mystery plots
- **Interactive fiction**: Enable games with sophisticated branching narratives
- **Educational tools**: Teach narrative structure and suspense techniques

### Potential Concerns
- Generated content should be clearly labeled as AI-generated
- System could potentially be misused for disinformation (multiple "truths")
- We will release with responsible use guidelines

---

## 8. Related Work

### Long-Form Story Generation
- DOC (Yang et al., 2022): Detailed outline control
- Re3 (Yang et al., 2022): Recursive reprompting
- CONCOCT (Mirowski et al., 2023): Collaborative story generation

### Plot and Narrative Planning
- PlotMachines (Rashkin et al., 2020): Outline-based generation
- STORIUM (Akoury et al., 2020): Game-based story generation
- Dramatron (Mirowski et al., 2023): Hierarchical drama generation

### Mystery and Suspense
- Limited prior work specifically on mystery generation
- Our work is the first to explicitly model dual-layer knowledge and suspense

---

## 9. Conclusion

SmokeMirror addresses a significant gap in narrative AI: the generation of structurally complex mystery fiction with dual perspectives and managed suspense. By introducing collision detection, discovery path management, and multi-perspective evaluation, we enable LLMs to produce stories with the sophisticated dramatic irony that defines the mystery genre.

---

## References

[To be added based on final related work review]

---

## Appendix: Example Output Structure

```
outputs/test_32b_YYYYMMDD_HHMMSS/
├── story.md                    # Final dual-layer narrative
├── plot_points.json            # Structured plot with suspense levels
├── facts.json                  # Real + fabricated facts
├── metrics.json                # Automatic evaluation scores
├── reader_evaluations.json     # Multi-perspective reader feedback
└── pipeline_logs/              # Generation intermediate steps
    ├── pipeline_summary.json
    ├── crime_backstory_*.json
    ├── plot_point_*.json
    └── reader_eval_*.json
```
