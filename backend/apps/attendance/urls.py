from rest_framework.routers import DefaultRouter
from .views import AttendanceViewset

router = DefaultRouter()
router.register("", AttendanceViewset, basename="attendance")

urlpatterns = router.urls
