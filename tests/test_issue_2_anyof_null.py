import pytest
from openapi_downgrade.converter.transformer import convert_spec

def test_anyof_null_with_ref():
    """
    Issue #2: anyOf containing type: null and a $ref should convert to allOf + nullable: true
    instead of anyOf with a nullable: true object.
    """
    spec = {
        "openapi": "3.1.0",
        "info": {"title": "Test Spec", "version": "1.0.0"},
        "paths": {},
        "components": {
            "schemas": {
                "SomeObject": {
                    "type": "object",
                    "properties": {"id": {"type": "integer"}}
                },
                "NullableRef": {
                    "anyOf": [
                        {"$ref": "#/components/schemas/SomeObject"},
                        {"type": "null"}
                    ]
                }
            }
        }
    }

    converted = convert_spec(spec)
    schema = converted["components"]["schemas"]["NullableRef"]

    # Check that anyOf is gone or correct
    if "anyOf" in schema:
        # If anyOf remains, it shouldn't have {nullable: true} as an isolated item
        for item in schema["anyOf"]:
            assert not (item.get("nullable") is True and len(item) == 1), \
                "Found isolated {nullable: true} in anyOf"
    
    # Check for correct resolution (allOf wrapping)
    assert converted["openapi"] == "3.0.3"
    assert schema.get("nullable") is True
    assert "allOf" in schema
    assert len(schema["allOf"]) == 1
    assert schema["allOf"][0]["$ref"] == "#/components/schemas/SomeObject"
    assert "anyOf" not in schema

def test_anyof_null_with_primitive():
    """
    anyOf containing type: null and a primitive should merge to type: primitive, nullable: true
    """
    spec = {
        "openapi": "3.1.0",
        "info": {"title": "Test Spec", "version": "1.0.0"},
        "paths": {},
        "components": {
            "schemas": {
                "NullableString": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "null"}
                    ]
                }
            }
        }
    }

    converted = convert_spec(spec)
    schema = converted["components"]["schemas"]["NullableString"]

    assert schema.get("nullable") is True
    assert schema.get("type") == "string"
    assert "anyOf" not in schema
