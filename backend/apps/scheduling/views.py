from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ClassSession
from .serializer import ClassSessionSerializer

class ClassSessionView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ClassSession.objects.all()
    serializer_class = ClassSessionSerializer

    def get_queryset(self):
        queryset = ClassSession.objects.filter(subject__course__teacher = self.request.user).order_by("date", "start_time")

        subject = self.request.query_params.get("subject")
        if subject:
            queryset = queryset.filter(subject__name__icontains = subject)

        date_from = self.request.query_params.get("date_from")
        if date_from:
            queryset = queryset.filter(date__gte = date_from)
        
        date_to = self.request.query_params.get("date__to")
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        return queryset
