from django.db.models import Q
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Audit
from .serializer import AuditSerializer


class AuditViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AuditSerializer

    def get_queryset(self):
        queryset = Audit.objects.filter(teacher=self.request.user).order_by("-timestamp")

        action = self.request.query_params.get("action")
        if action:
            queryset = queryset.filter(action__iexact=action)

        target_model = self.request.query_params.get("target_model")
        if target_model:
            queryset = queryset.filter(target_model__icontains=target_model)

        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(action__icontains=search)
                | Q(target_model__icontains=search)
                | Q(detail__icontains=search)
            )

        date_from = self.request.query_params.get("date_from")
        if date_from:
            parsed = parse_datetime(date_from) or parse_date(date_from)
            if parsed:
                queryset = queryset.filter(timestamp__gte=parsed)

        date_to = self.request.query_params.get("date_to")
        if date_to:
            parsed = parse_datetime(date_to) or parse_date(date_to)
            if parsed:
                queryset = queryset.filter(timestamp__lte=parsed)

        return queryset