from pydantic import ValidationError

from ppt_agent.models import DeckOutline, SlideSpec


def test_slide_bullets_trimmed() -> None:
    slide = SlideSpec(title="t", bullets=[" a ", "", "b"])
    assert slide.bullets == ["a", "b"]


def test_deck_requires_enough_slides() -> None:
    try:
        DeckOutline(topic="x", slides=[SlideSpec(title="only")])
    except ValidationError:
        return
    raise AssertionError("Expected validation error")


def test_deck_theme_defaults() -> None:
    outline = DeckOutline(
        topic="x",
        slides=[
            SlideSpec(title="1"),
            SlideSpec(title="2"),
            SlideSpec(title="3"),
        ],
    )
    assert outline.template == "consulting"
    assert outline.background == "light"
    assert len(outline.narrative_flow) >= 4


def test_theme_color_normalized() -> None:
    outline = DeckOutline(
        topic="x",
        theme_color="3b82f6",
        slides=[SlideSpec(title="1"), SlideSpec(title="2"), SlideSpec(title="3")],
    )
    assert outline.theme_color == "#3B82F6"


def test_content_outline_trimmed() -> None:
    outline = DeckOutline(
        topic="x",
        content_outline=[" 背景 ", "", "策略"],
        slides=[SlideSpec(title="1"), SlideSpec(title="2"), SlideSpec(title="3")],
    )
    assert outline.content_outline == ["背景", "策略"]
