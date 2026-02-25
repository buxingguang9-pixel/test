from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal


@dataclass
class Entity:
    text: str
    label: str


@dataclass
class Relation:
    head: str
    relation: str
    tail: str


@dataclass
class Event:
    trigger: str
    event_type: str


@dataclass
class OutputSchema:
    entities: list[Entity] = field(default_factory=list)
    relations: list[Relation] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "OutputSchema":
        entities = [Entity(**item) for item in data.get("entities", [])]
        relations = [Relation(**item) for item in data.get("relations", [])]
        events = [Event(**item) for item in data.get("events", [])]
        return cls(entities=entities, relations=relations, events=events)

    @staticmethod
    def json_schema() -> dict:
        return {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "label": {"type": "string"},
                        },
                        "required": ["text", "label"],
                    },
                },
                "relations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "head": {"type": "string"},
                            "relation": {"type": "string"},
                            "tail": {"type": "string"},
                        },
                        "required": ["head", "relation", "tail"],
                    },
                },
                "events": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "trigger": {"type": "string"},
                            "event_type": {"type": "string"},
                        },
                        "required": ["trigger", "event_type"],
                    },
                },
            },
            "required": ["entities", "relations", "events"],
        }

    def to_dict(self) -> dict:
        return {
            "entities": [asdict(item) for item in self.entities],
            "relations": [asdict(item) for item in self.relations],
            "events": [asdict(item) for item in self.events],
        }


@dataclass
class NEROnlySchema:
    entities: list[Entity] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "NEROnlySchema":
        entities = [Entity(**item) for item in data.get("entities", [])]
        return cls(entities=entities)

    @staticmethod
    def json_schema() -> dict:
        return {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "label": {"type": "string"},
                        },
                        "required": ["text", "label"],
                    },
                }
            },
            "required": ["entities"],
        }

    def to_dict(self) -> dict:
        return {"entities": [asdict(item) for item in self.entities]}


SchemaName = Literal["person_org_event", "ner_only"]
SchemaType = type[OutputSchema] | type[NEROnlySchema]


def get_schema(schema_name: SchemaName) -> SchemaType:
    if schema_name == "person_org_event":
        return OutputSchema
    return NEROnlySchema
