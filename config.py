from dataclasses import dataclass
import yaml


@dataclass
class ExperimentConfig:
    """
    Represents a parsed experiment configuration from a YAML file
    """
    name: str
    target: str
    failure: str
    duration_seconds: int
    health_check: str

def load_config(path: str) -> ExperimentConfig:
    """
    Reads a YAML experiment file and returns an ExperimentConfig object.
    Args:
        path: the file path to the YAML config file
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f)
        exp = data["experiment"]

    return ExperimentConfig(
        name=exp["name"],
        target=exp["target"],
        failure=exp["failure"],
        duration_seconds=exp["duration_seconds"],
        health_check=exp["health_check"]
    )

