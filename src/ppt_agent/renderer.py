from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from .models import DeckOutline, SlideSpec


@dataclass(frozen=True)
class ThemeSpec:
    bg_color: RGBColor
    title_color: RGBColor
    body_color: RGBColor
    accent_color: RGBColor
    title_font: str
    body_font: str


THEMES: dict[tuple[str, str], ThemeSpec] = {
    ("consulting", "light"): ThemeSpec(RGBColor(248, 250, 252), RGBColor(15, 23, 42), RGBColor(30, 41, 59), RGBColor(37, 99, 235), "Calibri", "Calibri"),
    ("consulting", "dark"): ThemeSpec(RGBColor(15, 23, 42), RGBColor(241, 245, 249), RGBColor(203, 213, 225), RGBColor(56, 189, 248), "Calibri", "Calibri"),
    ("consulting", "gradient"): ThemeSpec(RGBColor(239, 246, 255), RGBColor(3, 7, 18), RGBColor(51, 65, 85), RGBColor(79, 70, 229), "Calibri", "Calibri"),
    ("modern", "light"): ThemeSpec(RGBColor(255, 255, 255), RGBColor(17, 24, 39), RGBColor(55, 65, 81), RGBColor(14, 165, 233), "Aptos", "Aptos"),
    ("modern", "dark"): ThemeSpec(RGBColor(2, 6, 23), RGBColor(226, 232, 240), RGBColor(148, 163, 184), RGBColor(99, 102, 241), "Aptos", "Aptos"),
    ("modern", "gradient"): ThemeSpec(RGBColor(236, 253, 245), RGBColor(6, 78, 59), RGBColor(6, 95, 70), RGBColor(5, 150, 105), "Aptos", "Aptos"),
    ("minimal", "light"): ThemeSpec(RGBColor(250, 250, 250), RGBColor(38, 38, 38), RGBColor(64, 64, 64), RGBColor(115, 115, 115), "Arial", "Arial"),
    ("minimal", "dark"): ThemeSpec(RGBColor(23, 23, 23), RGBColor(245, 245, 245), RGBColor(212, 212, 212), RGBColor(163, 163, 163), "Arial", "Arial"),
    ("minimal", "gradient"): ThemeSpec(RGBColor(245, 245, 244), RGBColor(41, 37, 36), RGBColor(68, 64, 60), RGBColor(120, 113, 108), "Arial", "Arial"),
}


class PPTXRenderer:
    """Render structured slide specs to PPTX."""

    def render(self, outline: DeckOutline, output_path: Path) -> Path:
        presentation = Presentation()
        theme = THEMES[(outline.template, outline.background)]
        for index, slide in enumerate(outline.slides):
            self._render_slide(presentation=presentation, index=index, slide=slide, theme=theme)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        presentation.save(str(output_path))
        return output_path

    def _render_slide(self, presentation: Presentation, index: int, slide: SlideSpec, theme: ThemeSpec) -> None:
        if index == 0 or slide.layout == "title":
            self._render_title_slide(presentation, slide, theme)
            return
        if slide.layout == "section":
            self._render_section_slide(presentation, slide, theme)
            return
        if slide.layout == "comparison":
            self._render_comparison_slide(presentation, slide, theme)
            return
        self._render_content_slide(presentation, slide, theme)

    def _render_title_slide(self, presentation: Presentation, slide: SlideSpec, theme: ThemeSpec) -> None:
        ppt_slide = presentation.slides.add_slide(presentation.slide_layouts[0])
        self._apply_background(ppt_slide, theme)
        title_shape = ppt_slide.shapes.title
        title_shape.text = slide.title
        self._format_title(title_shape.text_frame, theme, size=42)
        if slide.subtitle and len(ppt_slide.placeholders) > 1:
            subtitle_shape = ppt_slide.placeholders[1]
            subtitle_shape.text = f"{slide.section}｜{slide.subtitle}" if slide.section else slide.subtitle
            self._format_subtitle(subtitle_shape.text_frame, theme)
        self._add_accent_bar(ppt_slide, theme)

    def _render_section_slide(self, presentation: Presentation, slide: SlideSpec, theme: ThemeSpec) -> None:
        ppt_slide = presentation.slides.add_slide(presentation.slide_layouts[5])
        self._apply_background(ppt_slide, theme)
        title = ppt_slide.shapes.title
        title.text = slide.section or slide.title
        self._format_title(title.text_frame, theme, size=44)
        if slide.subtitle:
            box = ppt_slide.shapes.add_textbox(Inches(1), Inches(3.0), Inches(11), Inches(1.2))
            frame = box.text_frame
            frame.text = slide.subtitle
            self._format_subtitle(frame, theme)
        self._add_accent_bar(ppt_slide, theme)

    def _render_content_slide(self, presentation: Presentation, slide: SlideSpec, theme: ThemeSpec) -> None:
        ppt_slide = presentation.slides.add_slide(presentation.slide_layouts[1])
        self._apply_background(ppt_slide, theme)
        title_text = f"{slide.section}｜{slide.title}" if slide.section else slide.title
        ppt_slide.shapes.title.text = title_text
        self._format_title(ppt_slide.shapes.title.text_frame, theme, size=32)

        body = ppt_slide.shapes.placeholders[1].text_frame
        body.clear()
        for line_id, bullet in enumerate(slide.bullets):
            paragraph = body.add_paragraph() if line_id > 0 else body.paragraphs[0]
            paragraph.text = bullet
            paragraph.level = 0
            paragraph.font.size = Pt(20)
            paragraph.font.name = theme.body_font
            paragraph.font.color.rgb = theme.body_color
            paragraph.space_after = Pt(8)
        self._add_accent_bar(ppt_slide, theme)

    def _render_comparison_slide(self, presentation: Presentation, slide: SlideSpec, theme: ThemeSpec) -> None:
        ppt_slide = presentation.slides.add_slide(presentation.slide_layouts[5])
        self._apply_background(ppt_slide, theme)
        title = ppt_slide.shapes.title
        title.text = f"{slide.section}｜{slide.title}" if slide.section else slide.title
        self._format_title(title.text_frame, theme, size=30)

        mid = max(1, len(slide.bullets) // 2)
        left_items = slide.bullets[:mid]
        right_items = slide.bullets[mid:]

        left_box = ppt_slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.4), Inches(4.6))
        right_box = ppt_slide.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.4), Inches(4.6))
        self._fill_comparison_box(left_box.text_frame, "维度 A", left_items, theme)
        self._fill_comparison_box(right_box.text_frame, "维度 B", right_items, theme)

        divider = ppt_slide.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.RECTANGLE,
            Inches(6.55),
            Inches(1.8),
            Inches(0.08),
            Inches(4.6),
        )
        divider.fill.solid()
        divider.fill.fore_color.rgb = theme.accent_color
        divider.line.fill.background()
        self._add_accent_bar(ppt_slide, theme)

    def _fill_comparison_box(self, text_frame, heading: str, items: list[str], theme: ThemeSpec) -> None:
        text_frame.clear()
        text_frame.text = heading
        for idx, para in enumerate(text_frame.paragraphs):
            para.font.bold = True
            para.font.name = theme.title_font
            para.font.size = Pt(18)
            para.font.color.rgb = theme.accent_color
            if idx == 0:
                para.space_after = Pt(10)

        for item in items or ["待补充对比要点"]:
            p = text_frame.add_paragraph()
            p.text = f"• {item}"
            p.font.name = theme.body_font
            p.font.size = Pt(16)
            p.font.color.rgb = theme.body_color
            p.space_after = Pt(6)

    def _add_accent_bar(self, ppt_slide, theme: ThemeSpec) -> None:
        bar = ppt_slide.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.RECTANGLE,
            Inches(0.0),
            Inches(0.0),
            Inches(13.33),
            Inches(0.12),
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = theme.accent_color
        bar.line.fill.background()

    def _apply_background(self, ppt_slide, theme: ThemeSpec) -> None:
        fill = ppt_slide.background.fill
        fill.solid()
        fill.fore_color.rgb = theme.bg_color

    def _format_title(self, text_frame, theme: ThemeSpec, size: int) -> None:
        for paragraph in text_frame.paragraphs:
            paragraph.font.bold = True
            paragraph.font.size = Pt(size)
            paragraph.font.name = theme.title_font
            paragraph.font.color.rgb = theme.title_color
            paragraph.alignment = PP_ALIGN.LEFT

    def _format_subtitle(self, text_frame, theme: ThemeSpec) -> None:
        for paragraph in text_frame.paragraphs:
            paragraph.font.size = Pt(20)
            paragraph.font.name = theme.body_font
            paragraph.font.color.rgb = theme.accent_color
            paragraph.alignment = PP_ALIGN.LEFT
