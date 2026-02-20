from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential


@dataclass(slots=True)
class GeminiClient:
    api_key: str
    model_name: str
    temperature: float = 0.4
    _model: Any = field(init=False, repr=False)

    def __post_init__(self) -> None:
        genai.configure(api_key=self.api_key)
        self._model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": self.temperature,
                "response_mime_type": "application/json",
            },
        )

    @retry(wait=wait_exponential(multiplier=1, min=1, max=8), stop=stop_after_attempt(3))
    def generate_json(self, prompt: str) -> dict:
        response = self._model.generate_content(prompt)
        text = response.text
        return json.loads(text)
