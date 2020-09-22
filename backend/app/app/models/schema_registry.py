import json
from typing import Type
from pydantic.main import BaseModel


def new_schema_registry(_schema_id: str, _id: str, _description: str, _key_or_value: str, _topic: str, _cls: Type[BaseModel]) -> dict:
    cls_schema = _cls.schema()
    schema_values = {
        "$schema": _schema_id,
        "$id": _id,
        "description": _description,

        "title": f"{_key_or_value}_{_topic}",

        "type": cls_schema["type"],
        "properties": cls_schema["properties"]
    }

    schema_registry = {
        "schema": json.dumps(schema_values),
        "schemaType": "JSON"
    }
    return schema_registry
