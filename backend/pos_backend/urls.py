from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.views import CategoryViewSet, ProductViewSet
from ai.views import AIInstructionView, AiLogViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"ai/logs", AiLogViewSet, basename="ai-log")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/ai/add-products/", AIInstructionView.as_view(), name="ai-add-products"),
]
