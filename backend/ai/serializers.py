from rest_framework import serializers

from .models import AiLog, AiParsedItem


class AiParsedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiParsedItem
        fields = [
            "id",
            "name",
            "category",
            "price",
            "stock",
            "status",
            "product_id",
            "error_message",
        ]


class AiLogSerializer(serializers.ModelSerializer):
    parsed_items = AiParsedItemSerializer(many=True, read_only=True)

    class Meta:
        model = AiLog
        fields = [
            "id",
            "raw_instruction",
            "ai_model",
            "ai_request",
            "ai_response",
            "status",
            "error_message",
            "parsed_items",
            "created_at",
        ]
        read_only_fields = fields
