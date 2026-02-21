from __future__ import annotations

from pathlib import Path

import typer

from .agent import PPTAgent
from .config import load_settings

app = typer.Typer(help="Gemini-powered PPT generation agent")


@app.command()
def generate(
    topic: str = typer.Option(..., help="PPT 主题"),
    audience: str = typer.Option("管理层", help="目标受众"),
    output: Path = typer.Option(Path("outputs/deck.pptx"), help="输出 PPTX 路径"),
    slide_count: int = typer.Option(8, min=3, max=30, help="页数"),
    style: str = typer.Option("executive", help="风格: executive|educational|marketing|technical"),
    template: str = typer.Option("consulting", help="模板: consulting|modern|minimal"),
    background: str = typer.Option("light", help="背景: light|dark|gradient"),
    theme_color: str | None = typer.Option(None, help="主题色（十六进制，如 #3B82F6）"),
    content_outline: list[str] | None = typer.Option(None, "--content-outline", help="自定义内容提纲，可多次传入"),
) -> None:
    settings = load_settings()
    agent = PPTAgent(settings)
    result = agent.run(
        topic=topic,
        audience=audience,
        output_path=output,
        slide_count=slide_count,
        style=style,
        template=template,
        background=background,
        theme_color=theme_color,
        content_outline=content_outline,
    )
    typer.echo(f"PPT 已生成: {result}")


if __name__ == "__main__":
    app()
