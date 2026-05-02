from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .models import Audit
from .serializer import AuditSerializer

class AuditViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer

    def get_queryset(self):
        queryset = Audit.objects.filter(teacher = self.request.user)

        return queryset