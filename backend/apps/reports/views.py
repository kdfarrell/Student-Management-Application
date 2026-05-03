from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.students.models import Student
from apps.courses.models import Course
from apps.scheduling.models import ClassSession
from apps.grades.models import Grade

from datetime import date, timedelta
from django.db.models import Count, Q, F, Avg, Case, When, ExpressionWrapper, FloatField


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        response = {}
 
        total_students = Student.objects.filter(teacher=request.user).count()
        response["total_students"] = total_students
    
        total_courses = Course.objects.filter(teacher=request.user).count()
        response["total_courses"] = total_courses

        if (date.today().weekday() == 6):
            week_start = date.today()
        else:
            week_start = date.today() - timedelta(days = (date.today().weekday() + 1))

        if (date.today().weekday() == 5):
            week_end = date.today()
        elif (date.today().weekday() == 6):
            week_end = date.today() + timedelta(days=6)
        else:
            week_end = date.today() + timedelta(days = (5 - date.today().weekday()))
        
        sessions_this_week = ClassSession.objects.filter(
            subject__course__teacher=request.user, 
            date__gte=week_start, 
            date__lte=week_end
        ).count()

        response["sessions_this_week"] = sessions_this_week


        at_risk_students_qs = Student.objects.annotate(
            attendance_count=Count('attendance'),
            present_count=Count('attendance', filter=Q(attendance__status="present")),
            avg_grade = Avg('grades__score')
        ).filter(
            teacher=request.user
        ).filter(
            Q(present_count__lt = F("attendance_count") * 0.75) |
            Q(avg_grade__lt = 50)
        )
    
        at_risk_count = at_risk_students_qs.count()
        at_risk_list = at_risk_students_qs.values(
            'first_name', 
            "last_name", 
            'avg_grade', 
            'present_count',
            'attendance_count'
        )

        response["at_risk_count"] = at_risk_count
        response["at_risk_list"] = at_risk_list


        grade_ranges = Grade.objects.filter(student__teacher = request.user).aggregate(
            range_0_49 = Count(Case(When(score__lt = 50, then=1))),
            range_50_69 = Count(Case(When(score__lt = 70, score__gt =49, then=1))),
            range_70_84 = Count(Case(When(score__lt = 85, score__gt = 69, then =1))),
            range_85_100 = Count(Case(When(score__gt = 84, then = 1)))
        )

        response["grade_ranges"] = grade_ranges


        attendance_overview_qs = Course.objects.annotate(
            course_attendance = Count('enrolled_students__student__attendance'),
            present_course_attendance = Count(
                'enrolled_students__student__attendance',
                filter = Q(enrolled_students__student__attendance__status='present')
            )
        ).filter(teacher = request.user).annotate(
            attendance_percentage = ExpressionWrapper(
                F('present_course_attendance') * 100 / F("course_attendance"),
                output_field=FloatField()
            )
        )

        attendance_overview_list = attendance_overview_qs.values(
            'name', 
            'course_attendance', 
            'present_course_attendance', 
            'attendance_percentage'
        )

        response["attendace_overview_list"] = attendance_overview_list


        return Response(response)
