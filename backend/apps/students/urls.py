from rest_framework.routers import DefaultRouter

from .views import StudentViewset

router = DefaultRouter()
router.register("students", StudentViewset, basename="students")

urlpatterns = router.urls