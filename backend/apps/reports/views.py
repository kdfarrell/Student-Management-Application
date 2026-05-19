import os
from datetime import date, timedelta
from decimal import Decimal
from io import BytesIO
from pathlib import Path

from django.core.mail import EmailMessage
from django.db.models import Avg, Case, Count, ExpressionWrapper, F, FloatField, Q, When
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from dotenv import load_dotenv
from pypdf import PdfWriter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from xhtml2pdf import pisa

from apps.attendance.models import Attendance
from apps.courses.models import Course, Enrollment
from apps.grades.models import Assessment, Grade
from apps.scheduling.models import ClassSession
from apps.students.models import Student

load_dotenv()


def generate_pdf(html_string):
    buffer = BytesIO()
    pisa.CreatePDF(html_string, dest=buffer)
    return buffer.getvalue()


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = {}

        total_students = Student.objects.filter(teacher=request.user).count()
        response["total_students"] = total_students

        total_courses = Course.objects.filter(teacher=request.user).count()
        response["total_courses"] = total_courses

        if date.today().weekday() == 6:
            week_start = date.today()
        else:
            week_start = date.today() - timedelta(days=(date.today().weekday() + 1))

        if date.today().weekday() == 5:
            week_end = date.today()
        elif date.today().weekday() == 6:
            week_end = date.today() + timedelta(days=6)
        else:
            week_end = date.today() + timedelta(days=(5 - date.today().weekday()))

        sessions_this_week = ClassSession.objects.filter(
            subject__course__teacher=request.user, date__gte=week_start, date__lte=week_end
        ).count()
        response["sessions_this_week"] = sessions_this_week

        at_risk_students_qs = (
            Student.objects.annotate(
                attendance_count=Count("attendance"),
                present_count=Count("attendance", filter=Q(attendance__status="present")),
                avg_grade=Avg("grades__score"),
            )
            .filter(teacher=request.user)
            .filter(Q(present_count__lt=F("attendance_count") * 0.75) | Q(avg_grade__lt=50))
        )

        at_risk_count = at_risk_students_qs.count()
        at_risk_list = at_risk_students_qs.values(
            "first_name", "last_name", "avg_grade", "present_count", "attendance_count"
        )

        response["at_risk_count"] = at_risk_count
        response["at_risk_list"] = at_risk_list

        grade_ranges = Grade.objects.filter(student__teacher=request.user).aggregate(
            range_0_49=Count(Case(When(score__lt=50, then=1))),
            range_50_69=Count(Case(When(score__lt=70, score__gt=49, then=1))),
            range_70_84=Count(Case(When(score__lt=85, score__gt=69, then=1))),
            range_85_100=Count(Case(When(score__gt=84, then=1))),
        )
        response["grade_ranges"] = grade_ranges

        # 1. Structural List Data for Course Breakdown Progress Bars
        attendance_overview_qs = (
            Course.objects.annotate(
                course_attendance=Count("enrolled_students__student__attendance"),
                present_course_attendance=Count(
                    "enrolled_students__student__attendance",
                    filter=Q(enrolled_students__student__attendance__status="present"),
                ),
            )
            .filter(teacher=request.user)
            .annotate(
                attendance_percentage=ExpressionWrapper(
                    F("present_course_attendance") * 100 / F("course_attendance"), output_field=FloatField()
                )
            )
        )
        response["attendance_overview_list"] = attendance_overview_qs.values(
            "name", "course_attendance", "present_course_attendance", "attendance_percentage"
        )

        # 2. Structural Doughnut Data Grouped By Assessment Types
        assessment_counts = (
            Assessment.objects.filter(subject__course__teacher=request.user)
            .values("assessment_type")
            .annotate(count=Count("id"))
        )
        assessment_map = {item["assessment_type"]: item["count"] for item in assessment_counts}
        
        response["assessment_distribution"] = {
            "test": assessment_map.get("test", 0),
            "assignment": assessment_map.get("assignment", 0),
            "exam": assessment_map.get("exam", 0),
            "quiz": assessment_map.get("quiz", 0),
        }

        return Response(response)


# --- Helper Functions for Reports ---


def build_grade_report_context(student, course, teacher):
    subjects = course.subjects.all()
    subject_data = []
    total_weighted_score = Decimal("0")
    total_weight = Decimal("0")

    for subject in subjects:
        assessments = Assessment.objects.filter(subject=subject)
        grades = Grade.objects.filter(student=student, assessment__in=assessments).select_related("assessment")

        grade_list = []
        subject_score = Decimal("0")
        subject_max = Decimal("0")

        for g in grades:
            pct = (g.score / g.assessment.max_score * 100) if g.assessment.max_score else Decimal("0")
            grade_list.append(
                {
                    "assessment": g.assessment,
                    "score": g.score,
                    "feedback": g.feedback,
                    "percentage": pct,
                }
            )
            subject_score += g.score
            subject_max += g.assessment.max_score

        avg = (subject_score / subject_max * 100) if subject_max else Decimal("0")

        if grade_list:
            total_weighted_score += avg * subject.weight
            total_weight += subject.weight

        subject_data.append(
            {
                "subject": subject,
                "grades": grade_list,
                "average": avg,
            }
        )

    overall_average = (total_weighted_score / total_weight) if total_weight else Decimal("0")

    return {
        "student": student,
        "course": course,
        "teacher": teacher,
        "subjects": subject_data,
        "overall_average": overall_average,
        "generated_on": timezone.now().strftime("%B %d, %Y at %I:%M %p"),
    }


def build_attendance_report_context(student, teacher):
    enrollments = Enrollment.objects.filter(student=student, status="active").select_related("course")
    course_data = []
    total_sessions_all = 0
    total_present_all = 0

    for enrollment in enrollments:
        course = enrollment.course
        records = (
            Attendance.objects.filter(student=student, session__subject__course=course)
            .select_related("session", "session__subject")
            .order_by("session__date")
        )

        total = records.count()
        present = records.filter(status__in=["present", "late"]).count()
        pct = (present / total * 100) if total else 0

        total_sessions_all += total
        total_present_all += present

        course_data.append(
            {
                "course": course,
                "records": records,
                "total_sessions": total,
                "present_count": present,
                "percentage": pct,
            }
        )

    overall_pct = (total_present_all / total_sessions_all * 100) if total_sessions_all else 0

    return {
        "student": student,
        "teacher": teacher,
        "courses": course_data,
        "total_sessions": total_sessions_all,
        "overall_percentage": overall_pct,
        "generated_on": timezone.now().strftime("%B %d, %Y at %I:%M %p"),
    }


# --- Report API Views ---


class GradeReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_id = request.query_params.get("student_id")
        course_id = request.query_params.get("course_id")

        if not student_id or not course_id:
            return Response({"error": "student_id and course_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(id=student_id, teacher=request.user)
            course = Course.objects.get(id=course_id, teacher=request.user)
        except (Student.DoesNotExist, Course.DoesNotExist):
            return Response({"error": "Student or Course not found."}, status=status.HTTP_404_NOT_FOUND)

        context = build_grade_report_context(student, course, request.user)
        html_string = render_to_string("reports/grade_report.html", context)
        pdf_file = generate_pdf(html_string)

        filename = f"grade_report_{student.last_name}_{course.name}.pdf".replace(" ", "_")
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class AttendanceReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_id = request.query_params.get("student_id")

        if not student_id:
            return Response({"error": "student_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(id=student_id, teacher=request.user)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        context = build_attendance_report_context(student, request.user)
        html_string = render_to_string("reports/attendance_report.html", context)
        pdf_file = generate_pdf(html_string)

        filename = f"attendance_report_{student.last_name}.pdf".replace(" ", "_")
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class CourseGradeReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        course_id = request.query_params.get("course_id")

        if not course_id:
            return Response({"error": "course_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id, teacher=request.user)
        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        enrollments = Enrollment.objects.filter(course=course, status="active").select_related("student")

        if not enrollments.exists():
            return Response({"error": "No enrolled students in this course."}, status=status.HTTP_404_NOT_FOUND)

        writer = PdfWriter()

        for enrollment in enrollments:
            student = enrollment.student
            context = build_grade_report_context(student, course, request.user)
            html_string = render_to_string("reports/grade_report.html", context)
            pdf_bytes = generate_pdf(html_string)
            writer.append(BytesIO(pdf_bytes))

        output = BytesIO()
        writer.write(output)
        output.seek(0)

        filename = f"course_grade_report_{course.name}.pdf".replace(" ", "_")
        response = HttpResponse(output.read(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class EmailReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student_id = request.data.get("student_id")
        course_id = request.data.get("course_id")
        report_type = request.data.get("report_type")  
        recipient_email = request.data.get("recipient_email")

        if not all([student_id, report_type, recipient_email]):
            return Response(
                {"error": "student_id, report_type, and recipient_email are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            student = Student.objects.get(id=student_id, teacher=request.user)
        except Student.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        if report_type == "grade":
            if not course_id:
                return Response(
                    {"error": "course_id is required for grade reports."}, status=status.HTTP_400_BAD_REQUEST
                )
            try:
                course = Course.objects.get(id=course_id, teacher=request.user)
            except Course.DoesNotExist:
                return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

            context = build_grade_report_context(student, course, request.user)
            html_string = render_to_string("reports/grade_report.html", context)
            pdf_bytes = generate_pdf(html_string)
            filename = f"grade_report_{student.last_name}_{course.name}.pdf".replace(" ", "_")
            subject_line = f"Grade Report – {student.first_name} {student.last_name} ({course.name})"

        elif report_type == "attendance":
            context = build_attendance_report_context(student, request.user)
            html_string = render_to_string("reports/attendance_report.html", context)
            pdf_bytes = generate_pdf(html_string)
            filename = f"attendance_report_{student.last_name}.pdf".replace(" ", "_")
            subject_line = f"Attendance Report – {student.first_name} {student.last_name}"

        else:
            return Response(
                {"error": "report_type must be 'grade' or 'attendance'."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            email = EmailMessage(
                subject=subject_line,
                body=f"Dear {recipient_email},\n\nPlease find attached the {report_type} report for {student.first_name} {student.last_name}.\n\nRegards,\n{request.user.first_name} {request.user.last_name}\n{request.user.school_name}",
                from_email=None,
                to=[recipient_email],
            )
            email.attach(filename, pdf_bytes, "application/pdf")
            email.send()
        except Exception as e:
            return Response({"error": f"Email failed to send: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Report sent successfully."}, status=status.HTTP_200_OK)