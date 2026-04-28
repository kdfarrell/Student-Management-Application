from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import StudentViewset

router = DefaultRouter()
router.register("", StudentViewset, basename="students")

urlpatterns = router.urls