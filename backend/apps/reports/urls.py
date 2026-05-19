from django.urls import include, path

from .views import (
    AttendanceReportView,
    CourseGradeReportView,
    DashboardView,
    EmailReportView,
    GradeReportView,
)

urlpatterns = [
    # Dashboard Route
    path("dashboard/", DashboardView.as_view(), name='dashboard'),

    # Report Routes
    path("grade/", GradeReportView.as_view(), name="grade-report"),
    path("attendance/", AttendanceReportView.as_view(), name="attendance-report"),
    path("course-grade/", CourseGradeReportView.as_view(), name="course-grade-report"),
    path("email/", EmailReportView.as_view(), name="email-report"),
]