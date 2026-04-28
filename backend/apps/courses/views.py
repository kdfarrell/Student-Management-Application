from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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
        serializer.save(teacher=self.request.user)


class SubjectViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()

    def get_queryset(self):
        queryset = Subject.objects.filter(course__teacher = self.request.user)

        return queryset


class EnrollmentViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.all()

    def get_queryset(self):
        queryset = Enrollment.objects.filter(course__teacher = self.request.user)

        return queryset

