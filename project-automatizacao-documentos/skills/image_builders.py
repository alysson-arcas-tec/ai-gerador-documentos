from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


def _font(size: int, bold: bool = False):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def build_timeline(scope_context: dict[str, Any], answers: dict[str, Any], output_path: Path, runtime: dict[str, Any]) -> Path:
    width = int(runtime["timeline"]["width"])
    height = int(runtime["timeline"]["height"])
    project_name = answers.get("project_name") or scope_context["project"].get("project_name") or "Projeto"
    start_date = datetime.strptime(answers["project_start_date"], "%d/%m/%Y")
    sprint_days = int(answers["sprint_length_days"])
    phases = answers["timeline_phases"]

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    left = 320
    top = 190
    row_height = 72
    weeks = sum(int(row["duration_sprints"]) for row in phases)
    step = max(120, (width - left - 120) / max(weeks, 1))

    draw.text((70, 50), f"Timeline - {project_name}", font=_font(36, True), fill="#1F4E79")
    draw.text((70, 98), f"Início do projeto: {answers['project_start_date']}", font=_font(18), fill="#64748B")
    draw.rounded_rectangle((60, 140, width - 60, height - 90), radius=20, outline="#D9E2EC", width=2)

    current = start_date
    for index in range(weeks + 1):
        x = int(left + index * step)
        draw.line((x, 155, x, height - 150), fill="#D9E2EC", width=1)
        if index < weeks:
            label = f"S{index + 1}\n{current.strftime('%d/%m')}"
            draw.multiline_text((x + 8, 150), label, font=_font(14, True), fill="#1F4E79", spacing=2)
            current = current + timedelta(days=sprint_days)

    current_start = start_date
    sprint_cursor = 0
    for row_index, row in enumerate(phases):
        y = top + row_index * row_height
        duration = int(row["duration_sprints"])
        x = int(left + sprint_cursor * step + 8)
        bar_width = int(duration * step - 16)
        current_end = current_start + timedelta(days=(duration * sprint_days) - 1)
        draw.text((80, y + 10), row["name"], font=_font(21, True), fill="#1F2933")
        draw.text((80, y + 38), row["objective"], font=_font(14), fill="#64748B")
        draw.rounded_rectangle((x, y + 12, x + bar_width, y + 50), radius=14, fill="#2E75B6")
        period_text = f"{current_start.strftime('%d/%m')} a {current_end.strftime('%d/%m')}"
        text_box = draw.textbbox((0, 0), period_text, font=_font(14, True))
        text_width = text_box[2] - text_box[0]
        draw.text((x + (bar_width - text_width) / 2, y + 23), period_text, font=_font(14, True), fill="white")
        current_start = current_end + timedelta(days=1)
        sprint_cursor += duration

    image.save(output_path)
    return output_path
