from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

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
        serializer.save(teacher=self.request.user)
