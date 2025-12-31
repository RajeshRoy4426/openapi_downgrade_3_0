import sys
import os
import json
import datetime

# Add current directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from openapi_downgrade.converter.transformer import convert_spec
from openapi_downgrade.converter.loader import _parse_spec, load_spec

def run_issue_1():
    print("Running Issue #1 (Datetime) test...")
    yaml_content = """
    openapi: 3.1.0
    info:
      title: Test Spec
      version: 1.0.0
      x-updated: 2024-11-24T10:30:00Z
    paths: {}
    """
    spec = _parse_spec(yaml_content)
    json_str = json.dumps(spec)
    assert "2024-11-24T10:30:00+00:00" in json_str or "2024-11-24T10:30:00Z" in json_str
    print("Issue #1 passed.")

def run_issue_2():
    print("Running Issue #2 (anyOf null) test...")
    spec = {
        "openapi": "3.1.0",
        "info": {"title": "Test Spec", "version": "1.0.0"},
        "paths": {},
        "components": {
            "schemas": {
                "NullableRef": {
                    "anyOf": [
                        {"$ref": "#/components/schemas/SomeObject"},
                        {"type": "null"}
                    ]
                },
                "SomeObject": {"type": "object"}
            }
        }
    }
    converted = convert_spec(spec)
    schema = converted["components"]["schemas"]["NullableRef"]
    assert schema.get("nullable") is True
    assert "allOf" in schema
    assert schema["allOf"][0]["$ref"] == "#/components/schemas/SomeObject"
    assert "anyOf" not in schema
    print("Issue #2 passed.")

def run_existing_rules():
    print("Running basic rules tests...")
    from openapi_downgrade.converter.rules.mixed_types import convert_mixed_types
    assert convert_mixed_types({"type": ["string", "number"]}) == {"oneOf": [{"type": "string"}, {"type": "number"}]}
    
    from openapi_downgrade.converter.rules.nullable import convert_nullable
    assert convert_nullable({"type": ["string", "null"]}) == {"type": "string", "nullable": True}
    
    print("Basic rules tests passed.")

if __name__ == "__main__":
    try:
        run_issue_1()
        run_issue_2()
        run_existing_rules()
        print("\nAll targeted tests passed!")
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
