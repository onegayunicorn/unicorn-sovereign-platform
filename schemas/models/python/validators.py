import json
import jsonschema
from pathlib import Path

SCHEMA_DIR = Path(__file__).parent.parent.parent

def load_schema(name: str) -> dict:
    path = SCHEMA_DIR / f"{name}.schema.json"
    with open(path) as f:
        return json.load(f)

def validate_against_schema(instance: dict, schema_name: str) -> tuple[bool, str]:
    try:
        schema = load_schema(schema_name)
        jsonschema.validate(instance=instance, schema=schema)
        return True, "OK"
    except jsonschema.ValidationError as e:
        return False, f"VALIDATION FAILED: {e.message}"
    except FileNotFoundError:
        return False, f"SCHEMA NOT FOUND: {schema_name}"
