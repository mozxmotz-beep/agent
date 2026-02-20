from pathlib import Path

from ppt_agent.models import DeckOutline, SlideSpec
from ppt_agent.renderer import PPTXRenderer


def test_renderer_output(tmp_path: Path) -> None:
    outline = DeckOutline(
        topic="demo",
        slides=[
            SlideSpec(title="封面", subtitle="副标题", layout="title"),
            SlideSpec(title="要点", bullets=["A", "B"], layout="title_and_content"),
            SlideSpec(title="结论", bullets=["C"], layout="title_and_content"),
        ],
    )
    renderer = PPTXRenderer()
    target = tmp_path / "deck.pptx"
    renderer.render(outline, target)
    assert target.exists()
