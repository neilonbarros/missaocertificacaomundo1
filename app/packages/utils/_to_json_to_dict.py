import json
from typing import Any


def to_json_do_dict(
    value: str,
) -> dict[str, Any]:
    return json.loads(value)
