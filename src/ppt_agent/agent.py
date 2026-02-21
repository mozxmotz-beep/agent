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
    ) -> DeckOutline:
        count = slide_count or self.settings.default_slide_count
        prompt = render_template(
            "outline_prompt.txt",
            topic=topic,
            audience=audience,
            slide_count=count,
            style=style,
            template=template,
            background=background,
        )
        payload = self.client.generate_json(prompt)
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
    ) -> Path:
        outline = self.create_outline(
            topic=topic,
            audience=audience,
            slide_count=slide_count,
            style=style,
            template=template,
            background=background,
        )
        return self.renderer.render(outline=outline, output_path=output_path)
