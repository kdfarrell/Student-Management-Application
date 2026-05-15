from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ClassSession
from .serializer import ClassSessionSerializer

class ClassSessionView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassSessionSerializer
    queryset = ClassSession.objects.all()

    def get_queryset(self):

        # Get sessions for courses taught by the logged-in teacher
        user = self.request.user
        queryset = ClassSession.objects.filter(subject__course__teacher=user).order_by("date", "start_time")

        # Filter by subject name if provided
        subject = self.request.query_params.get("subject")
        if subject:
            queryset = queryset.filter(subject__name__icontains=subject)

        # Filter by date ranges
        date_from = self.request.query_params.get("date_from")
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        
        date_to = self.request.query_params.get("date_to") or self.request.query_params.get("date__to")
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        return queryset

    def perform_create(self, serializer):
        serializer.save()