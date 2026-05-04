from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .utils import read_json


@dataclass
class AgentDefinition:
    agent_id: str
    title: str
    builder: str
    output_format: str
    default_output: str
    prompt_file: str
    summary: str

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "AgentDefinition":
        return cls(
            agent_id=payload["id"],
            title=payload["title"],
            builder=payload["builder"],
            output_format=payload["output_format"],
            default_output=payload["default_output"],
            prompt_file=payload["prompt_file"],
            summary=payload["summary"],
        )


def load_registry(root: Path) -> dict[str, AgentDefinition]:
    agents_dir = root / "agents"
    registry: dict[str, AgentDefinition] = {}
    for path in sorted(agents_dir.glob("*.json")):
        agent = AgentDefinition.from_payload(read_json(path))
        registry[agent.agent_id] = agent
    return registry
