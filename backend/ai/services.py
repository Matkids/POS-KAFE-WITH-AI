from typing import Dict

from rest_framework import serializers

from common.exceptions import AIClientError, AIResponseValidationError
from products.serializers import ProductSerializer
from products.services import ProductService

from .ai_client import AIClient
from .models import AiLog, AiParsedItem


class AIService:
    def __init__(self):
        self.client = AIClient()

    def process_instruction(self, instruction: str) -> Dict:
        log = AiLog.objects.create(raw_instruction=instruction, ai_model=self.client.model_name)
        try:
            response = self.client.generate_products(instruction)
            log.ai_request = self.client.last_request
            log.ai_response = response

            items = response.get("items")
            if not isinstance(items, list):
                raise AIResponseValidationError("AI response must contain an 'items' list")
            if not items:
                raise AIResponseValidationError("No products detected from your instruction")

            inserted, failed = self._persist_items(log, items)
            log.status = self._derive_status(inserted, failed)
            log.save(update_fields=["ai_request", "ai_response", "status"])
            return {"log_id": log.id, "inserted": inserted, "failed": failed}
        except (AIClientError, AIResponseValidationError, serializers.ValidationError) as exc:
            log.status = AiLog.STATUS_FAILED
            log.error_message = str(exc)
            log.save(update_fields=["status", "error_message", "ai_request", "ai_response"])
            raise

    def _persist_items(self, log: AiLog, items):
        inserted, failed = [], []
        for item in items:
            parsed = AiParsedItem.objects.create(
                ai_log=log,
                name=item.get("name"),
                category=item.get("category"),
                price=item.get("price"),
                stock=item.get("stock"),
            )
            try:
                product = ProductService.create_product(
                    {
                        "name": item.get("name"),
                        "price": item.get("price"),
                        "stock": item.get("stock", 0),
                        "category_name": item.get("category"),
                    }
                )
                parsed.status = AiParsedItem.STATUS_INSERTED
                parsed.product = product
                parsed.save(update_fields=["status", "product"])
                inserted.append(ProductSerializer(product).data)
            except Exception as exc:
                parsed.status = AiParsedItem.STATUS_FAILED
                parsed.error_message = str(exc)
                parsed.save(update_fields=["status", "error_message"])
                failed.append({"name": item.get("name"), "reason": str(exc)})
        return inserted, failed

    @staticmethod
    def _derive_status(inserted, failed):
        if inserted and failed:
            return AiLog.STATUS_PARTIAL
        if inserted:
            return AiLog.STATUS_SUCCESS
        return AiLog.STATUS_FAILED
