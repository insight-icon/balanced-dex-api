import json
from typing import Type

from app.models.rwmodel import RWModel
from pydantic.main import BaseModel


# class SchemaRegistry(RWModel):
#     schema: str
#     schemaType: str


# class Schema(RWModel):
#     # $schema: str
#     schema_id: str
#     # $id: str
#     id: str
#     description: str
#
#     title: str
#     type: str
#     properties: dict


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

    # schema_registry = SchemaRegistry(schema=json.dumps(schema_values), schema_type="JSON")
    schema_registry = {
        "schema": json.dumps(schema_values),
        "schemaType": "JSON"
    }
    return schema_registry
