from rest_framework.routers import DefaultRouter

from .views import AiLogViewSet

router = DefaultRouter()
router.register(r"logs", AiLogViewSet, basename="ai-log")

urlpatterns = router.urls
