# Colab PPT Agent（Gemini）

一个可在 **Google Colab** 运行的工程化 PPT 生成 Agent，流程参考 Manus 的“规划 + 执行”模式：

1. **Planner（Gemini）**：将用户主题转成结构化大纲 JSON。
2. **Renderer（python-pptx）**：把大纲稳定渲染成 `.pptx` 文件。

## 项目结构

```text
.
├── prompts/
│   └── outline_prompt.txt
├── src/ppt_agent/
│   ├── agent.py
│   ├── cli.py
│   ├── config.py
│   ├── gemini_client.py
│   ├── models.py
│   ├── prompts.py
│   └── renderer.py
├── tests/
│   ├── test_models.py
│   └── test_renderer.py
└── pyproject.toml
```

## Colab 快速开始

在 Colab 单元执行：

```python
!git clone <your_repo_url>
%cd agent
!pip install -e .

import os
os.environ["GEMINI_API_KEY"] = "你的 Gemini Key"
os.environ["GEMINI_MODEL"] = "gemini-1.5-pro"

!ppt-agent generate --topic "AI赋能企业经营分析" --audience "CEO与业务负责人" --slide-count 8 --output outputs/ai_strategy.pptx
```

下载文件：

```python
from google.colab import files
files.download("outputs/ai_strategy.pptx")
```

## 工程化特性

- **强类型数据模型**：Pydantic 约束 LLM 输出，避免脏数据进入渲染。
- **失败重试**：Gemini 请求自动指数退避重试。
- **Prompt 模板化**：提示词文件独立，便于 A/B 迭代。
- **CLI 与模块解耦**：可本地调试，也可无缝放入 Colab。

## 后续可扩展

- 增加图表生成器（Mermaid/Matplotlib）并注入幻灯片。
- 增加企业模板库（主题色、版式、字体映射）。
- 增加“审校 Agent”，自动检查逻辑链路与口径一致性。
