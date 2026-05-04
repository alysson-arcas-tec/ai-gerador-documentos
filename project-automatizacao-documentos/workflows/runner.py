from __future__ import annotations

from pathlib import Path
from typing import Any

from skills.agent_registry import AgentDefinition, load_registry
from skills.docx_builders import DOCX_BUILDERS
from skills.image_builders import build_timeline
from skills.questionnaire import collect_answers, export_answers_template
from skills.scope_reader import read_scope
from skills.utils import ensure_dir, read_json, slugify
from skills.xlsx_builders import build_backlog, build_cycle_details


BUILDERS = {
    **DOCX_BUILDERS,
    "timeline_png": build_timeline,
    "sprint_backlog": build_backlog,
    "cycle_details": build_cycle_details,
}


class AgentRunner:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.registry = load_registry(root)
        self.runtime = read_json(root / "config" / "runtime.json")
        self.aliases = self._load_aliases()
        self.lookup = self._build_lookup()

    def _load_aliases(self) -> dict[str, list[str]]:
        aliases_path = self.root / "config" / "agent_aliases.json"
        if not aliases_path.exists():
            return {}
        payload = read_json(aliases_path)
        return {key: list(value) for key, value in payload.items()}

    def _candidate_terms(self, agent: AgentDefinition) -> set[str]:
        terms = {
            agent.agent_id,
            agent.title,
            agent.default_output,
            Path(agent.default_output).stem,
        }
        for alias in self.aliases.get(agent.agent_id, []):
            terms.add(alias)
        return {term for term in terms if term}

    def _build_lookup(self) -> dict[str, str]:
        lookup: dict[str, str] = {}
        for agent in self.registry.values():
            for term in self._candidate_terms(agent):
                lookup[slugify(term)] = agent.agent_id
        return lookup

    def list_agents(self) -> list[AgentDefinition]:
        return list(self.registry.values())

    def get_agent(self, agent_ref: str) -> AgentDefinition:
        if agent_ref in self.registry:
            return self.registry[agent_ref]
        resolved_id = self.lookup.get(slugify(agent_ref))
        if not resolved_id:
            available = ", ".join(sorted(self.registry))
            raise KeyError(f"Agente nao encontrado: {agent_ref}. Disponiveis: {available}")
        return self.registry[resolved_id]

    def export_template(self, agent_id: str, scope_path: Path, target_path: Path) -> Path:
        agent = self.get_agent(agent_id)
        scope_context = read_scope(scope_path, self.root / "assets")
        return export_answers_template(self.root / "prompts" / agent.prompt_file, scope_context, target_path)

    def run(
        self,
        agent_id: str,
        scope_path: Path,
        output_path: Path | None = None,
        answers_path: Path | None = None,
        interactive: bool = True,
    ) -> Path:
        agent = self.get_agent(agent_id)
        scope_context = read_scope(scope_path, self.root / "assets")
        provided_answers: dict[str, Any] | None = None
        if answers_path:
            provided_answers = read_json(answers_path)

        answers = collect_answers(
            self.root / "prompts" / agent.prompt_file,
            scope_context,
            provided_answers=provided_answers,
            interactive=interactive,
        )
        builder = BUILDERS[agent.builder]
        final_output = output_path or (Path.cwd() / agent.default_output)
        ensure_dir(final_output.parent)
        return builder(scope_context, answers, final_output, self.runtime)
