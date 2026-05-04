from __future__ import annotations

from pathlib import Path
from typing import Any

from .utils import coerce_scalar, lookup_path, read_json, value_present, write_json


def _default_value(field: dict[str, Any], scope_context: dict[str, Any], current: dict[str, Any]) -> Any:
    for source_key in field.get("source_keys", []):
        value = lookup_path(scope_context, source_key)
        if value_present(value):
            return value
    if "default" in field:
        return field["default"]
    if field.get("default_from_answer"):
        value = current.get(field["default_from_answer"])
        if value_present(value):
            return value
    return None


def _table_from_source(field: dict[str, Any], scope_context: dict[str, Any]) -> list[dict[str, Any]] | None:
    for source_key in field.get("source_keys", []):
        source = lookup_path(scope_context, source_key)
        if isinstance(source, list) and source:
            rows: list[dict[str, Any]] = []
            for item in source:
                row: dict[str, Any] = {column["name"]: "" for column in field.get("columns", [])}
                for column in field.get("columns", []):
                    source_name = column.get("source_name", column["name"])
                    if isinstance(item, dict) and source_name in item:
                        row[column["name"]] = item[source_name]
                rows.append(row)
            return rows
    if field.get("default_rows_data"):
        return field["default_rows_data"]
    return None


def _prompt_text(label: str, default: Any = None) -> str:
    suffix = f" [{default}]" if value_present(default) else ""
    return input(f"{label}{suffix}: ").strip()


def _ask_table(field: dict[str, Any], default_rows: list[dict[str, Any]] | None, interactive: bool) -> list[dict[str, Any]]:
    columns = field.get("columns", [])
    if default_rows and not interactive:
        return default_rows
    if default_rows and interactive:
        use_default = _prompt_text(f"{field['label']} - usar linhas sugeridas do escopo? (s/n)", "s")
        if use_default.lower() in {"", "s", "sim", "y", "yes"}:
            rows: list[dict[str, Any]] = []
            for index, default_row in enumerate(default_rows, start=1):
                row: dict[str, Any] = {}
                print(f"\nLinha {index} de {field['label']}")
                for column in columns:
                    current = default_row.get(column["name"])
                    answer = _prompt_text(column["label"], current)
                    row[column["name"]] = answer or current or ""
                rows.append(row)
            return rows
    if not interactive:
        raise ValueError(f"Campo obrigatório sem resposta: {field['name']}")
    count_raw = _prompt_text(f"{field['label']} - quantidade de linhas", field.get("default_rows", 1))
    count = int(count_raw or field.get("default_rows", 1))
    rows = []
    for index in range(1, count + 1):
        row: dict[str, Any] = {}
        print(f"\nLinha {index} de {field['label']}")
        for column in columns:
            row[column["name"]] = coerce_scalar(_prompt_text(column["label"]), column.get("type", "text"))
        rows.append(row)
    return rows


def collect_answers(
    prompts_path: Path,
    scope_context: dict[str, Any],
    provided_answers: dict[str, Any] | None = None,
    interactive: bool = True,
) -> dict[str, Any]:
    prompt_spec = read_json(prompts_path)
    answers = dict(provided_answers or {})
    missing: list[str] = []
    for field in prompt_spec.get("fields", []):
        if value_present(answers.get(field["name"])):
            continue
        if field["type"] == "table":
            default_rows = _table_from_source(field, scope_context)
            try:
                answers[field["name"]] = _ask_table(field, default_rows, interactive)
            except ValueError:
                missing.append(field["name"])
            continue

        default = _default_value(field, scope_context, answers)
        if value_present(default) and not field.get("always_prompt", False):
            answers[field["name"]] = default
            continue

        if not interactive:
            missing.append(field["name"])
            continue

        raw = _prompt_text(field["label"], default)
        if not raw and value_present(default):
            answers[field["name"]] = default
        else:
            answers[field["name"]] = coerce_scalar(raw, field["type"])

    if missing:
        raise ValueError("Campos obrigatórios ausentes: " + ", ".join(missing))
    return answers


def export_answers_template(prompts_path: Path, scope_context: dict[str, Any], target_path: Path) -> Path:
    prompt_spec = read_json(prompts_path)
    template: dict[str, Any] = {}
    for field in prompt_spec.get("fields", []):
        if field["type"] == "table":
            source_rows = _table_from_source(field, scope_context)
            if source_rows:
                template[field["name"]] = source_rows
            else:
                template[field["name"]] = [
                    {column["name"]: "" for column in field.get("columns", [])}
                ]
        elif field["type"] == "list":
            default = _default_value(field, scope_context, template)
            template[field["name"]] = default if value_present(default) else []
        else:
            default = _default_value(field, scope_context, template)
            template[field["name"]] = default if value_present(default) else ""
    write_json(target_path, template)
    return target_path
