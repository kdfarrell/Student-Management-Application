from rest_framework.routers import DefaultRouter

from .views import AuditViewset

router = DefaultRouter()
router.register("", AuditViewset, basename="audit")

urlpatterns = router.urls