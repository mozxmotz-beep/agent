from __future__ import annotations

from pathlib import Path

from pptx import Presentation

from .models import DeckOutline, SlideSpec


class PPTXRenderer:
    """Render structured slide specs to PPTX."""

    def __init__(self) -> None:
        self.presentation = Presentation()

    def render(self, outline: DeckOutline, output_path: Path) -> Path:
        for index, slide in enumerate(outline.slides):
            self._render_slide(index=index, slide=slide)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.presentation.save(str(output_path))
        return output_path

    def _render_slide(self, index: int, slide: SlideSpec) -> None:
        if index == 0 or slide.layout == "title":
            layout = self.presentation.slide_layouts[0]
            ppt_slide = self.presentation.slides.add_slide(layout)
            ppt_slide.shapes.title.text = slide.title
            if slide.subtitle and len(ppt_slide.placeholders) > 1:
                ppt_slide.placeholders[1].text = slide.subtitle
            return

        layout = self.presentation.slide_layouts[1]
        ppt_slide = self.presentation.slides.add_slide(layout)
        ppt_slide.shapes.title.text = slide.title
        body = ppt_slide.shapes.placeholders[1].text_frame
        body.clear()
        for line_id, bullet in enumerate(slide.bullets):
            paragraph = body.add_paragraph() if line_id > 0 else body.paragraphs[0]
            paragraph.text = bullet
            paragraph.level = 0
