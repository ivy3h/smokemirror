"""
Data structures for representing crime facts, story elements, and evaluation results.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class CharacterRole(Enum):
    """Roles a character can play in the story."""
    CRIMINAL = "criminal"
    CONSPIRATOR = "conspirator"
    VICTIM = "victim"
    DETECTIVE = "detective"
    WITNESS = "witness"
    SUSPECT = "suspect"
    BYSTANDER = "bystander"


class EvidenceType(Enum):
    """Types of evidence in the story."""
    PHYSICAL = "physical"
    TESTIMONIAL = "testimonial"
    DOCUMENTARY = "documentary"
    DIGITAL = "digital"
    CIRCUMSTANTIAL = "circumstantial"


class IssueSeverity(Enum):
    """Severity levels for issues found during evaluation."""
    MINOR = "minor"
    MODERATE = "moderate"
    CRITICAL = "critical"


class IssueType(Enum):
    """Types of issues that can be flagged during evaluation."""
    LOGICAL_INCONSISTENCY = "logical_inconsistency"
    PACING_ISSUE = "pacing_issue"
    SUSPENSE_DROP = "suspense_drop"
    LAYER_LEAK = "layer_leak"
    CHARACTER_IMPLAUSIBILITY = "character_implausibility"
    TROPE_OVERUSE = "trope_overuse"
    RED_HERRING_TRANSPARENT = "red_herring_transparent"


@dataclass
class Character:
    """Represents a character in the story."""
    name: str
    role: CharacterRole
    occupation: str
    motive: Optional[str] = None
    means: Optional[str] = None
    opportunity: Optional[str] = None
    alibi: Optional[str] = None
    secret: Optional[str] = None  # Hidden information about the character
    leverage: Optional[str] = None  # What keeps conspirators loyal
    relationship_to_victim: Optional[str] = None
    is_conspirator: bool = False

    def has_mmo(self) -> bool:
        """Check if character has means, motive, and opportunity."""
        return all([self.means, self.motive, self.opportunity])

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "role": self.role.value,
            "occupation": self.occupation,
            "motive": self.motive,
            "means": self.means,
            "opportunity": self.opportunity,
            "alibi": self.alibi,
            "secret": self.secret,
            "leverage": self.leverage,
            "relationship_to_victim": self.relationship_to_victim,
            "is_conspirator": self.is_conspirator,
        }


@dataclass
class Evidence:
    """Represents a piece of evidence."""
    id: str
    description: str
    evidence_type: EvidenceType
    location: str
    discovered_by: Optional[str] = None
    is_planted: bool = False
    real_meaning: Optional[str] = None  # What it actually proves
    fabricated_meaning: Optional[str] = None  # What conspirators want detective to think

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "type": self.evidence_type.value,
            "location": self.location,
            "discovered_by": self.discovered_by,
            "is_planted": self.is_planted,
            "real_meaning": self.real_meaning,
            "fabricated_meaning": self.fabricated_meaning,
        }


@dataclass
class Timeline:
    """Represents a timeline of events."""
    events: list[dict] = field(default_factory=list)
    # Each event: {"time": str, "description": str, "actor": str, "location": str}

    def add_event(self, time: str, description: str, actor: str, location: str):
        self.events.append({
            "time": time,
            "description": description,
            "actor": actor,
            "location": location,
        })

    def to_dict(self) -> dict:
        return {"events": self.events}


@dataclass
class CrimeFacts:
    """The real crime facts - what actually happened."""
    crime_type: str
    victim: Character
    criminal: Character
    conspirators: list[Character]
    motive: str
    method: str
    timeline: Timeline
    evidence: list[Evidence]
    location: str
    coordination_plan: str  # How conspirators coordinate their cover-up

    def to_dict(self) -> dict:
        return {
            "crime_type": self.crime_type,
            "victim": self.victim.to_dict(),
            "criminal": self.criminal.to_dict(),
            "conspirators": [c.to_dict() for c in self.conspirators],
            "motive": self.motive,
            "method": self.method,
            "timeline": self.timeline.to_dict(),
            "evidence": [e.to_dict() for e in self.evidence],
            "location": self.location,
            "coordination_plan": self.coordination_plan,
        }


@dataclass
class FabricatedFacts:
    """The fabricated crime narrative - what conspirators want detective to believe."""
    fake_suspect: Character
    fake_motive: str
    fake_method: str
    fake_timeline: Timeline
    planted_evidence: list[Evidence]
    alibis: dict[str, str]  # character_name -> alibi
    cover_story: str

    def to_dict(self) -> dict:
        return {
            "fake_suspect": self.fake_suspect.to_dict(),
            "fake_motive": self.fake_motive,
            "fake_method": self.fake_method,
            "fake_timeline": self.fake_timeline.to_dict(),
            "planted_evidence": [e.to_dict() for e in self.planted_evidence],
            "alibis": self.alibis,
            "cover_story": self.cover_story,
        }


@dataclass
class DiscoveryPath:
    """A potential way the detective could discover the truth."""
    id: str
    description: str
    involves_character: Optional[str] = None
    involves_evidence: Optional[str] = None
    difficulty: int = 5  # 1-10, how hard to discover
    is_open: bool = True
    closed_by: Optional[str] = None  # Plot point that closed this path

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "involves_character": self.involves_character,
            "involves_evidence": self.involves_evidence,
            "difficulty": self.difficulty,
            "is_open": self.is_open,
            "closed_by": self.closed_by,
        }


@dataclass
class PlotPoint:
    """A single plot point in the story."""
    id: int
    description: str
    detective_action: Optional[str] = None
    conspirator_intervention: Optional[str] = None
    obstacle: Optional[str] = None
    reader_revelation: Optional[str] = None  # What reader learns about real crime
    detective_learns: Optional[str] = None  # What detective learns (from fabricated layer)
    paths_closed: list[str] = field(default_factory=list)
    suspense_level: int = 5
    is_collision: bool = False  # Did detective get close to truth?

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "detective_action": self.detective_action,
            "conspirator_intervention": self.conspirator_intervention,
            "obstacle": self.obstacle,
            "reader_revelation": self.reader_revelation,
            "detective_learns": self.detective_learns,
            "paths_closed": self.paths_closed,
            "suspense_level": self.suspense_level,
            "is_collision": self.is_collision,
        }


@dataclass
class StoryState:
    """Current state of the story generation."""
    reader_knowledge: set = field(default_factory=set)  # Facts reader knows
    detective_knowledge: set = field(default_factory=set)  # Facts detective knows
    discovery_paths: list[DiscoveryPath] = field(default_factory=list)
    suspense_level: int = 5
    plot_points: list[PlotPoint] = field(default_factory=list)
    current_phase: str = "investigation"  # investigation, climax, resolution

    def get_open_paths(self) -> list[DiscoveryPath]:
        return [p for p in self.discovery_paths if p.is_open]

    def close_path(self, path_id: str, closed_by: str):
        for path in self.discovery_paths:
            if path.id == path_id:
                path.is_open = False
                path.closed_by = closed_by


@dataclass
class ReaderEvaluation:
    """Evaluation from a simulated reader."""
    reader_role: str
    suspense_scores: dict[int, float]  # plot_point_id -> score
    criminal_predictions: dict[int, dict]  # checkpoint -> {"prediction": str, "reasoning": str}
    inconsistency_flags: list[dict]  # [{"plot_point": int, "issue": str, "severity": IssueSeverity}]
    engagement_assessment: dict  # {"most_engaging": list, "least_engaging": list, "comments": str}
    overall_score: float

    def to_dict(self) -> dict:
        return {
            "reader_role": self.reader_role,
            "suspense_scores": self.suspense_scores,
            "criminal_predictions": self.criminal_predictions,
            "inconsistency_flags": [
                {**f, "severity": f["severity"].value if isinstance(f["severity"], IssueSeverity) else f["severity"]}
                for f in self.inconsistency_flags
            ],
            "engagement_assessment": self.engagement_assessment,
            "overall_score": self.overall_score,
        }


@dataclass
class RevisionDirective:
    """A directive for revising a specific part of the story."""
    target_plot_points: list[int]
    issue_type: IssueType
    severity: IssueSeverity
    description: str
    suggested_revision: str
    consensus_count: int  # How many readers flagged this
    priority: float  # Computed priority score

    def to_dict(self) -> dict:
        return {
            "target_plot_points": self.target_plot_points,
            "issue_type": self.issue_type.value,
            "severity": self.severity.value,
            "description": self.description,
            "suggested_revision": self.suggested_revision,
            "consensus_count": self.consensus_count,
            "priority": self.priority,
        }
