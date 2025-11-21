from django.db import models

from products.models import Product


class AiLog(models.Model):
    STATUS_PENDING = "pending"
    STATUS_SUCCESS = "success"
    STATUS_PARTIAL = "partial"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "pending"),
        (STATUS_SUCCESS, "success"),
        (STATUS_PARTIAL, "partial"),
        (STATUS_FAILED, "failed"),
    ]

    raw_instruction = models.TextField()
    ai_model = models.CharField(max_length=100, blank=True, null=True)
    ai_request = models.JSONField(blank=True, null=True)
    ai_response = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_PENDING)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"AI Log {self.id} - {self.status}"


class AiParsedItem(models.Model):
    STATUS_PENDING = "pending"
    STATUS_INSERTED = "inserted"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "pending"),
        (STATUS_INSERTED, "inserted"),
        (STATUS_FAILED, "failed"),
    ]

    ai_log = models.ForeignKey(AiLog, on_delete=models.CASCADE, related_name="parsed_items")
    name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_PENDING)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"Parsed {self.name or 'item'} ({self.status})"
