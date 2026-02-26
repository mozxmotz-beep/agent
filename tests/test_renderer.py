from pathlib import Path

from pptx import Presentation

from ppt_agent.models import DeckOutline, SlideSpec
from ppt_agent.renderer import PPTXRenderer


def test_renderer_output(tmp_path: Path) -> None:
    outline = DeckOutline(
        topic="demo",
        template="modern",
        background="dark",
        slides=[
            SlideSpec(title="封面", subtitle="副标题", layout="title", section="开场"),
            SlideSpec(title="现状综述", subtitle="关键事实", layout="section", section="现状"),
            SlideSpec(title="方案比较", bullets=["成本", "时效", "风险", "收益"], layout="comparison", section="策略"),
        ],
    )
    renderer = PPTXRenderer()
    target = tmp_path / "deck.pptx"
    renderer.render(outline, target)
    assert target.exists()

    result = Presentation(str(target))
    assert len(result.slides) == 3
    assert result.slides[0].shapes.title.text == "封面"
    assert result.slides[1].shapes.title.text == "现状"
    assert "策略｜方案比较" in result.slides[2].shapes.title.text


def test_renderer_is_stateless_across_multiple_renders(tmp_path: Path) -> None:
    outline = DeckOutline(
        topic="demo",
        slides=[SlideSpec(title="封面", layout="title"), SlideSpec(title="页2"), SlideSpec(title="页3")],
    )
    renderer = PPTXRenderer()
    one = tmp_path / "one.pptx"
    two = tmp_path / "two.pptx"

    renderer.render(outline, one)
    renderer.render(outline, two)

    first = Presentation(str(one))
    second = Presentation(str(two))
    assert len(first.slides) == 3
    assert len(second.slides) == 3
