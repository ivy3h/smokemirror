"""
Configuration management for Smokemirror.
"""

import yaml
import os
from dataclasses import dataclass, field
from typing import Optional
import random
import numpy as np
import torch


@dataclass
class ModelConfig:
    """Model configuration."""
    name: str = "Qwen/Qwen3-8B"
    device: str = "auto"
    load_in_4bit: bool = True
    load_in_8bit: bool = False
    torch_dtype: str = "bfloat16"
    max_new_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    do_sample: bool = True
    repetition_penalty: float = 1.1


@dataclass
class GenerationConfig:
    """Story generation configuration."""
    min_plot_points: int = 15
    max_plot_points: int = 25
    min_conspirators: int = 2
    max_conspirators: int = 4
    min_suspects: int = 3
    max_suspects: int = 6
    discovery_paths_threshold: int = 1
    initial_discovery_paths: int = 5


@dataclass
class SuspenseConfig:
    """Suspense controller configuration."""
    initial_level: int = 3
    max_level: int = 10
    path_close_probability: float = 0.7
    new_path_probability: float = 0.2
    collision_check_sensitivity: float = 0.5


@dataclass
class ReaderRole:
    """Configuration for a reader role."""
    name: str
    focus: str
    weight: float = 1.0


@dataclass
class ReaderSimulationConfig:
    """Reader simulation configuration."""
    enabled: bool = True
    num_readers: int = 3
    reader_roles: list[ReaderRole] = field(default_factory=list)
    checkpoints: list[int] = field(default_factory=lambda: [5, 10, 15])
    suspense_threshold: float = 6.0


@dataclass
class RefinementConfig:
    """Refinement configuration."""
    max_iterations: int = 3
    consensus_threshold: int = 2
    critical_issue_weight: float = 3.0
    moderate_issue_weight: float = 1.5
    minor_issue_weight: float = 0.5


@dataclass
class OutputConfig:
    """Output configuration."""
    save_intermediate: bool = True
    output_dir: str = "outputs"
    format: str = "markdown"


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    save_logs: bool = True


@dataclass
class Config:
    """Main configuration class."""
    model: ModelConfig = field(default_factory=ModelConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    suspense: SuspenseConfig = field(default_factory=SuspenseConfig)
    reader_simulation: ReaderSimulationConfig = field(default_factory=ReaderSimulationConfig)
    refinement: RefinementConfig = field(default_factory=RefinementConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    seed: int = 42

    def set_seed(self):
        """Set random seeds for reproducibility."""
        random.seed(self.seed)
        np.random.seed(self.seed)
        torch.manual_seed(self.seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(self.seed)


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "configs",
            "default.yaml"
        )

    with open(config_path, "r") as f:
        yaml_config = yaml.safe_load(f)

    # Parse model config
    model_cfg = ModelConfig(**yaml_config.get("model", {}))

    # Parse generation config
    gen_cfg = GenerationConfig(**yaml_config.get("generation", {}))

    # Parse suspense config
    suspense_cfg = SuspenseConfig(**yaml_config.get("suspense", {}))

    # Parse reader simulation config
    reader_yaml = yaml_config.get("reader_simulation", {})
    reader_roles = [
        ReaderRole(**role) for role in reader_yaml.get("reader_roles", [])
    ]
    reader_cfg = ReaderSimulationConfig(
        enabled=reader_yaml.get("enabled", True),
        num_readers=reader_yaml.get("num_readers", 3),
        reader_roles=reader_roles,
        checkpoints=reader_yaml.get("checkpoints", [5, 10, 15]),
        suspense_threshold=reader_yaml.get("suspense_threshold", 6.0),
    )

    # Parse refinement config
    ref_cfg = RefinementConfig(**yaml_config.get("refinement", {}))

    # Parse output config
    out_cfg = OutputConfig(**yaml_config.get("output", {}))

    # Parse logging config
    log_cfg = LoggingConfig(**yaml_config.get("logging", {}))

    return Config(
        model=model_cfg,
        generation=gen_cfg,
        suspense=suspense_cfg,
        reader_simulation=reader_cfg,
        refinement=ref_cfg,
        output=out_cfg,
        logging=log_cfg,
        seed=yaml_config.get("seed", 42),
    )
