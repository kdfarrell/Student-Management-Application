from rest_framework.routers import DefaultRouter

from .views import AssessmentViewset, GradeViewset

router = DefaultRouter()
router.register("assessments", AssessmentViewset)
router.register("grades", GradeViewset)

urlpatterns = router.urls