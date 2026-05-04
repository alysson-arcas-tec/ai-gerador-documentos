from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from workflows.runner import AgentRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Runner local dos agentes de automação de documentos."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-agents", help="Lista os agentes disponíveis.")

    describe = subparsers.add_parser("describe", help="Exibe detalhes de um agente.")
    describe.add_argument("agent_id")

    export = subparsers.add_parser("export-template", help="Exporta um template JSON de respostas.")
    export.add_argument("agent_id")
    export.add_argument("--scope", required=True)
    export.add_argument("--output", required=True)

    run = subparsers.add_parser("run", help="Executa um agente.")
    run.add_argument("agent_id")
    run.add_argument("--scope", required=True)
    run.add_argument("--output")
    run.add_argument("--answers")
    run.add_argument("--non-interactive", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    runner = AgentRunner(ROOT)

    if args.command == "list-agents":
        for agent in runner.list_agents():
            print(f"{agent.agent_id}: {agent.title} -> {agent.default_output}")
        return 0

    if args.command == "describe":
        agent = runner.get_agent(args.agent_id)
        print(f"ID: {agent.agent_id}")
        print(f"Título: {agent.title}")
        print(f"Formato: {agent.output_format}")
        print(f"Saída padrão: {agent.default_output}")
        print(f"Prompt: {agent.prompt_file}")
        print(f"Resumo: {agent.summary}")
        return 0

    if args.command == "export-template":
        target = runner.export_template(args.agent_id, Path(args.scope), Path(args.output))
        print(target)
        return 0

    if args.command == "run":
        target = runner.run(
            args.agent_id,
            Path(args.scope),
            output_path=Path(args.output) if args.output else None,
            answers_path=Path(args.answers) if args.answers else None,
            interactive=not args.non_interactive,
        )
        print(target)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
