# Prompt Engineering 信息提取与 JSON 格式化研究项目

本仓库提供两部分内容：

1. **可用于“提示工程优化的信息提取 + JSON 格式化”研究的数据集清单**（含任务类型、语言、下载入口与研究建议）。
2. **一个可直接扩展的 Python 项目模板**，用于：
   - 构建提示词（包含 schema 约束与 few-shot 示例）
   - 调用模型（示例里使用 `MockLLMClient`，可替换为真实 API）
   - 清洗并校验模型输出 JSON

---

## 1) 推荐数据集

完整结构化版本见：`data/datasets_catalog.json`。

重点推荐（按研究常见性）：

- **DocRED**：文档级关系抽取（英文）
- **SciERC**：科技论文命名实体与关系抽取（英文）
- **ACE2005**：实体/关系/事件抽取（英文，需授权）
- **CoNLL-2003**：经典 NER（英文）
- **DuIE 2.0**：中文关系抽取（百度）
- **People's Daily NER**：中文 NER（常见开源版本）
- **MIT Movie / MIT Restaurant**：面向槽位抽取与结构化输出
- **SQuAD 2.0**（可转信息抽取场景）：问答到结构化字段映射

---

## 2) 项目结构

```text
.
├── data/
│   └── datasets_catalog.json
├── src/
│   └── prompt_ie_json/
│       ├── __init__.py
│       ├── extractor.py
│       ├── main.py
│       ├── prompts.py
│       └── schema.py
├── tests/
│   └── test_extractor.py
└── README.md
```

---

## 3) 快速开始

无需额外三方依赖（仅 Python 3.10+）。

运行示例：

```bash
python -m src.prompt_ie_json.main \
  --text "OpenAI 于 2023 年发布了新模型，总部位于旧金山。" \
  --schema person_org_event
```

运行测试：

```bash
python -m pytest -q
```

---

## 4) 如何替换为真实大模型 API

当前 `extractor.py` 中使用了 `MockLLMClient` 来确保离线可运行。
你可以将 `LLMClient.generate` 接口替换为真实模型调用（如 OpenAI、Azure OpenAI、vLLM、本地模型服务）。

建议保留以下机制以提升 JSON 结构稳定性：

- 明确 schema 字段与类型（在提示词中显式声明）
- 要求“仅输出 JSON，不要解释文本”
- 后处理阶段对代码块、前后噪声进行清洗
- 使用数据类（dataclass）进行输出结构校验

---

## 5) 研究建议（面向论文或实验）

可围绕以下变量做消融实验：

- 提示模板：zero-shot / few-shot / chain-of-thought（隐式）
- 约束强度：自然语言约束 vs JSON Schema 约束
- 输出修复：无修复 / 规则修复 / 模型自修复
- 评估指标：
  - IE：Precision / Recall / F1
  - JSON：解析成功率、schema 通过率、字段级准确率

