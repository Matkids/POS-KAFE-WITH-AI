import json
from typing import Any, Dict

from rest_framework import serializers


def parse_json(content: str) -> Dict[str, Any]:
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:  # pragma: no cover - simple message
        raise serializers.ValidationError(f"Unable to parse AI response as JSON: {exc}")
