import json
import yaml
import requests
from pathlib import Path
from datetime import date, datetime

def load_spec(path_or_url: str) -> dict:
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        response = requests.get(path_or_url)
        response.raise_for_status()
        return _parse_spec(response.text)
    else:
        path = Path(path_or_url)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return _parse_spec(f.read())

def _parse_spec(text: str) -> dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = yaml.safe_load(text)
    
    return _convert_datetime_objects(data)

def _convert_datetime_objects(obj):
    """
    Recursively convert datetime and date objects to ISO format strings.
    """
    if isinstance(obj, dict):
        return {k: _convert_datetime_objects(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_datetime_objects(item) for item in obj]
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    else:
        return obj
