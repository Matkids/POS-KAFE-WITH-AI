from typing import Dict, Optional

from rest_framework import serializers

from common import validators
from .models import Category, Product


def _resolve_category(category: Optional[Category], category_name: Optional[str]):
    if category:
        return category
    if not category_name:
        return None
    name = category_name.strip()
    obj, _ = Category.objects.get_or_create(name=name)
    return obj


class ProductService:
    @staticmethod
    def create_product(payload: Dict) -> Product:
        name = (payload.get("name") or "").strip()
        if not name:
            raise serializers.ValidationError("Product name is required")

        price = validators.validate_price(validators.normalize_price(payload.get("price")))
        stock = validators.validate_stock(payload.get("stock", 0))
        category = payload.get("category")
        category_name = payload.get("category_name") or payload.get("category_text")
        category = _resolve_category(category, category_name)

        if Product.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError("Product with this name already exists")

        return Product.objects.create(
            name=name,
            price=price,
            stock=stock,
            sku=payload.get("sku"),
            category=category,
            is_active=payload.get("is_active", True),
        )

    @staticmethod
    def update_product(product: Product, payload: Dict) -> Product:
        if "name" in payload:
            name = (payload.get("name") or "").strip()
            if not name:
                raise serializers.ValidationError("Product name is required")
            if Product.objects.exclude(id=product.id).filter(name__iexact=name).exists():
                raise serializers.ValidationError("Product with this name already exists")
            product.name = name

        if "price" in payload:
            product.price = validators.validate_price(validators.normalize_price(payload.get("price")))

        if "stock" in payload:
            product.stock = validators.validate_stock(payload.get("stock", product.stock))

        if "category" in payload or payload.get("category_name"):
            category = payload.get("category")
            category_name = payload.get("category_name")
            product.category = _resolve_category(category, category_name)

        if "sku" in payload:
            product.sku = payload.get("sku") or None

        if "is_active" in payload:
            product.is_active = bool(payload.get("is_active"))

        product.save()
        return product
