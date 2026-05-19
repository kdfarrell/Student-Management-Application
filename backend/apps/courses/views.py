from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.audit.utils import log_audit

from .models import Course, Subject, Enrollment
from .serializer import CourseSerializer, SubjectSerializer, EnrollmentSerializer

class CourseViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        queryset = Course.objects.filter(teacher = self.request.user)

        return queryset
    
    def perform_create(self, serializer):
        course = serializer.save(teacher=self.request.user)
        log_audit(
            teacher=self.request.user,
            action="create",
            target_model="Course",
            target_id=course.id,
            detail={"name": course.name},
        )

    def perform_update(self, serializer):
        course = serializer.save()
        log_audit(
            teacher=self.request.user,
            action="update",
            target_model="Course",
            target_id=course.id,
            detail={"name": course.name},
        )

    def perform_destroy(self, instance):
        log_audit(
            teacher=self.request.user,
            action="delete",
            target_model="Course",
            target_id=instance.id,
            detail={"name": instance.name},
        )
        instance.delete()


class SubjectViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()

    def get_queryset(self):
        queryset = Subject.objects.filter(course__teacher = self.request.user)

        return queryset

    def perform_create(self, serializer):
        subject = serializer.save()
        log_audit(
            teacher=self.request.user,
            action="create",
            target_model="Subject",
            target_id=subject.id,
            detail={"name": subject.name, "course": subject.course.name},
        )

    def perform_update(self, serializer):
        subject = serializer.save()
        log_audit(
            teacher=self.request.user,
            action="update",
            target_model="Subject",
            target_id=subject.id,
            detail={"name": subject.name, "course": subject.course.name},
        )

    def perform_destroy(self, instance):
        log_audit(
            teacher=self.request.user,
            action="delete",
            target_model="Subject",
            target_id=instance.id,
            detail={"name": instance.name, "course": instance.course.name},
        )
        instance.delete()


class EnrollmentViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.all()

    def get_queryset(self):
        queryset = Enrollment.objects.filter(course__teacher=self.request.user)
        
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course__id=course_id)
        
        return queryset

    def perform_create(self, serializer):
        enrollment = serializer.save()
        log_audit(
            teacher=self.request.user,
            action="create",
            target_model="Enrollment",
            target_id=enrollment.id,
            detail={
                "student": f"{enrollment.student.first_name} {enrollment.student.last_name}",
                "course": enrollment.course.name,
            },
        )

    def perform_destroy(self, instance):
        log_audit(
            teacher=self.request.user,
            action="delete",
            target_model="Enrollment",
            target_id=instance.id,
            detail={
                "student": f"{instance.student.first_name} {instance.student.last_name}",
                "course": instance.course.name,
            },
        )
        instance.delete()

