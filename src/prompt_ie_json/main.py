from __future__ import annotations

import argparse
import json

from .extractor import InformationExtractor, MockLLMClient
from .schema import get_schema


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prompt IE + JSON formatting demo")
    parser.add_argument("--text", required=True, help="输入文本")
    parser.add_argument(
        "--schema",
        choices=["person_org_event", "ner_only"],
        default="person_org_event",
        help="输出 schema 类型",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    schema_model = get_schema(args.schema)

    extractor = InformationExtractor(llm_client=MockLLMClient())
    result = extractor.extract(text=args.text, schema_model=schema_model)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
