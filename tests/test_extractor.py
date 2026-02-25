from src.prompt_ie_json.extractor import InformationExtractor, MockLLMClient
from src.prompt_ie_json.schema import OutputSchema


def test_extract_returns_valid_schema() -> None:
    extractor = InformationExtractor(llm_client=MockLLMClient())
    result = extractor.extract(
        text="OpenAI 于 2023 年发布了新模型，总部位于旧金山。",
        schema_model=OutputSchema,
    )

    assert len(result.entities) >= 1
    assert any(rel.relation == "headquartered_in" for rel in result.relations)


def test_strip_to_json_handles_fenced_block() -> None:
    raw = """说明\n```json
{"entities": [], "relations": [], "events": []}
```\n结束"""
    cleaned = InformationExtractor._strip_to_json(raw)
    assert cleaned.startswith("{")
    assert cleaned.endswith("}")
