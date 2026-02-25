from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from .prompts import build_extraction_prompt
from .schema import NEROnlySchema, OutputSchema, SchemaType


@dataclass
class LLMClient:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class MockLLMClient(LLMClient):
    """离线演示用模型客户端，返回一个稳定 JSON。"""

    def generate(self, prompt: str) -> str:
        _ = prompt
        return json.dumps(
            {
                "entities": [
                    {"text": "OpenAI", "label": "ORG"},
                    {"text": "旧金山", "label": "LOC"},
                    {"text": "2023年", "label": "DATE"},
                ],
                "relations": [
                    {"head": "OpenAI", "relation": "headquartered_in", "tail": "旧金山"}
                ],
                "events": [
                    {"trigger": "发布", "event_type": "product_release"}
                ],
            },
            ensure_ascii=False,
        )


class InformationExtractor:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    @staticmethod
    def _strip_to_json(text: str) -> str:
        code_block = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.DOTALL)
        if code_block:
            return code_block.group(1)

        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("模型输出中未找到 JSON 对象")
        return text[start : end + 1]

    def extract(
        self,
        text: str,
        schema_model: SchemaType,
        few_shot_examples: list[dict] | None = None,
    ) -> OutputSchema | NEROnlySchema:
        schema_dict: dict[str, Any] = schema_model.json_schema()
        prompt = build_extraction_prompt(
            text=text,
            schema_dict=schema_dict,
            few_shot_examples=few_shot_examples,
        )
        raw_output = self.llm_client.generate(prompt)
        json_text = self._strip_to_json(raw_output)
        parsed = json.loads(json_text)
        return schema_model.from_dict(parsed)
