import datetime
import json
import yaml
from openapi_downgrade.converter.loader import _parse_spec

def test_datetime_serialization_error():
    """
    Issue #1: YAML loader might produce datetime objects which cause JSON serialization errors.
    """
    # Simulate a YAML content that might be parsed as datetime
    # Note: standard yaml.safe_load typically parses ISO timestamps as datetime objects
    yaml_content = """
    openapi: 3.1.0
    info:
      title: Test Spec
      version: 1.0.0
      x-updated: 2024-11-24T10:30:00Z
    paths: {}
    """
    
    # Verify that yaml.safe_load actually produces a datetime object here
    parsed = yaml.safe_load(yaml_content)
    assert isinstance(parsed["info"]["x-updated"], datetime.datetime)

    # Now verify that our tool handles this gracefully (or currently fails)
    # The fix should ensure _parse_spec or the dumper handles it.
    
    # We'll test _parse_spec directly first, though the error happens at json.dump time usually.
    # The issue states: "Conversion fails with Error: Object of type datetime is not JSON serializable"
    
    # So we need to ensure that the object returned by load_spec/convert_spec is fully serializable
    
    try:
        spec = _parse_spec(yaml_content)
        # Attempt to dump to JSON
        json.dumps(spec) 
    except TypeError as e:
        if "datetime" in str(e) and "not JSON serializable" in str(e):
            print("Reproduction successful: TypeError detected.")
            raise AssertionError("Reproduced expected failure") from e
    
    print("Test passed (or failed to reproduce if no error)")

if __name__ == "__main__":
    try:
        test_datetime_serialization_error()
    except AssertionError:
        pass # Expected reproduction
