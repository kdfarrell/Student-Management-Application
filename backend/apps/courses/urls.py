from rest_framework.routers import DefaultRouter

from .views import SubjectViewset, CourseViewset, EnrollmentViewset

router = DefaultRouter()

router.register("subjects", SubjectViewset, basename="subjects")
router.register("courses", CourseViewset, basename="courses")
router.register("enrollment", EnrollmentViewset, basename="enrollment")

urlpatterns = router.urls