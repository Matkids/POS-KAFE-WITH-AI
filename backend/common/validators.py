import re
from typing import Any

from rest_framework import serializers


def normalize_price(value: Any) -> int:
    if value is None or value == "":
        raise serializers.ValidationError("Price is required")

    if isinstance(value, (int, float)):
        price = int(value)
    else:
        raw = str(value).lower().replace("rp", "").replace(",", "").strip()
        if raw.endswith("k"):
            raw = raw[:-1]
            price = int(float(raw) * 1000)
        else:
            cleaned = re.sub(r"[^0-9]", "", raw)
            if not cleaned:
                raise serializers.ValidationError("Price must be numeric")
            price = int(cleaned)

    return validate_price(price)


def validate_price(price: Any) -> int:
    try:
        price_int = int(price)
    except (TypeError, ValueError):
        raise serializers.ValidationError("Price must be a number")

    if price_int <= 0:
        raise serializers.ValidationError("Price must be greater than zero")
    return price_int


def validate_stock(stock: Any) -> int:
    try:
        stock_int = int(stock)
    except (TypeError, ValueError):
        raise serializers.ValidationError("Stock must be a number")

    if stock_int < 0:
        raise serializers.ValidationError("Stock cannot be negative")
    return stock_int


def normalize_text(value: Any) -> str:
    return str(value).strip() if value is not None else ""
