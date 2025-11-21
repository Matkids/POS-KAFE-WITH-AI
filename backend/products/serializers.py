from rest_framework import serializers

from common import validators
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True, required=False, allow_null=True
    )
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "category_id",
            "category_name",
            "price",
            "stock",
            "sku",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "category"]

    def validate_name(self, value: str) -> str:
        if not value or not value.strip():
            raise serializers.ValidationError("Name is required")
        return value.strip()

    def validate_price(self, value):
        return validators.validate_price(value)

    def validate_stock(self, value):
        return validators.validate_stock(value)

    def to_internal_value(self, data):
        if "price" in data:
            data = data.copy()
            data["price"] = validators.normalize_price(data.get("price"))
        return super().to_internal_value(data)
