from __future__ import annotations

from pathlib import Path
from string import Template

PROMPT_DIR = Path(__file__).resolve().parents[2] / "prompts"


def load_prompt(name: str) -> str:
    prompt_path = PROMPT_DIR / name
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def render_template(name: str, **kwargs: str | int) -> str:
    template = Template(load_prompt(name))
    return template.safe_substitute(**kwargs)
