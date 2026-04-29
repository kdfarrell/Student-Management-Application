from rest_framework.routers import DefaultRouter

from .views import ClassSessionView

router = DefaultRouter()
router.register("", ClassSessionView, basename="class_session")

urlpatterns = router.urls