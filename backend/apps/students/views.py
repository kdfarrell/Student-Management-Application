from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


from rest_framework.decorators import action
from rest_framework.response import Response
from apps.scheduling.models import ClassSession
from apps.attendance.models import Attendance


from apps.audit.utils import log_audit

from .models import Student
from .serializer import StudentSerializer

class StudentViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.filter(teacher=self.request.user)

        is_active = self.request.query_params.get('is_active')

        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(is_active=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(is_active=False)

        name = self.request.query_params.get("search")
    
        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) | Q(last_name__icontains=name)
            )

        return queryset
    
    
    def perform_create(self, serializer):
        student = serializer.save(teacher=self.request.user)
        log_audit(
            teacher=self.request.user,
            action="create",
            target_model="Student",
            target_id=student.id,
            detail={"name": f"{student.first_name} {student.last_name}"},
        )

    def perform_update(self, serializer):
        student = serializer.save()
        log_audit(
            teacher=self.request.user,
            action="update",
            target_model="Student",
            target_id=student.id,
            detail={"name": f"{student.first_name} {student.last_name}"},
        )

    def perform_destroy(self, instance):
        log_audit(
            teacher=self.request.user,
            action="delete",
            target_model="Student",
            target_id=instance.id,
            detail={"name": f"{instance.first_name} {instance.last_name}"},
        )
        instance.delete()

    @action(detail=True, methods=["get"], url_path="attendance-summary")
    def attendance_summary(self, request, pk=None):
        student = self.get_object()
        
        enrollments = student.enrollments.filter(status="active")
        
        summary = []
        for enrollment in enrollments:
            course = enrollment.course
            sessions = ClassSession.objects.filter(subject__course=course)
            total = sessions.count()
            present = Attendance.objects.filter(
                student=student,
                session__in=sessions,
                status="present"
            ).count()
            percentage = (present / total * 100) if total > 0 else 0
            
            summary.append({
                "course": course.name,
                "total_sessions": total,
                "present": present,
                "percentage": round(percentage, 2)
            })
        
        return Response(summary)
