from __future__ import annotations

import json


def build_extraction_prompt(text: str, schema_dict: dict, few_shot_examples: list[dict] | None = None) -> str:
    examples_block = ""
    if few_shot_examples:
        rendered = []
        for idx, ex in enumerate(few_shot_examples, start=1):
            rendered.append(
                f"示例{idx}输入:\n{ex['input']}\n示例{idx}输出:\n{json.dumps(ex['output'], ensure_ascii=False)}"
            )
        examples_block = "\n\n" + "\n\n".join(rendered)

    schema_text = json.dumps(schema_dict, ensure_ascii=False, indent=2)

    return (
        "你是一个信息抽取系统。请从给定文本中提取实体、关系与事件，并严格输出 JSON。\n"
        "要求：\n"
        "1) 仅输出 JSON 对象，不要输出额外解释。\n"
        "2) 字段必须符合给定 schema。\n"
        "3) 若没有对应信息，返回空数组。\n\n"
        f"目标 schema:\n{schema_text}"
        f"{examples_block}\n\n"
        f"待抽取文本:\n{text}"
    )
