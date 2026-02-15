import json
from pathlib import Path
from jsonschema import validate, ValidationError


SCHEMA_PATH = Path(__file__).parents[1] / "schemas" / "worker_result.schema.json"


def validate_worker_result(payload: dict) -> None:
    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    try:
        validate(instance=payload, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Invalid worker result: {e.message}") from e
