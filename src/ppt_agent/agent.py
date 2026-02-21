from __future__ import annotations

from pathlib import Path

from .config import Settings
from .gemini_client import GeminiClient
from .models import DeckOutline
from .prompts import render_template
from .renderer import PPTXRenderer


class PPTAgent:
    """Planner + renderer pipeline for PPT generation."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = GeminiClient(
            api_key=settings.gemini_api_key,
            model_name=settings.gemini_model,
            temperature=settings.temperature,
        )
        self.renderer = PPTXRenderer()

    def create_outline(
        self,
        topic: str,
        audience: str,
        slide_count: int | None = None,
        style: str = "executive",
        template: str = "consulting",
        background: str = "light",
        theme_color: str | None = None,
        content_outline: list[str] | None = None,
    ) -> DeckOutline:
        count = slide_count or self.settings.default_slide_count
        outline_hint = "\n".join(f"- {item}" for item in (content_outline or [])) or "（未指定）"
        prompt = render_template(
            "outline_prompt.txt",
            topic=topic,
            audience=audience,
            slide_count=count,
            style=style,
            template=template,
            background=background,
            theme_color=theme_color or "default",
            content_outline=outline_hint,
        )
        payload = self.client.generate_json(prompt)
        payload.setdefault("theme_color", theme_color)
        payload.setdefault("content_outline", content_outline or [])
        return DeckOutline.model_validate(payload)

    def run(
        self,
        topic: str,
        audience: str,
        output_path: Path,
        slide_count: int | None = None,
        style: str = "executive",
        template: str = "consulting",
        background: str = "light",
        theme_color: str | None = None,
        content_outline: list[str] | None = None,
    ) -> Path:
        outline = self.create_outline(
            topic=topic,
            audience=audience,
            slide_count=slide_count,
            style=style,
            template=template,
            background=background,
            theme_color=theme_color,
            content_outline=content_outline,
        )
        return self.renderer.render(outline=outline, output_path=output_path)
