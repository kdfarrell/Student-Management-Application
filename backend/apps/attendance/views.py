from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Attendance
from .serializer import AttendanceSerializer

class AttendanceViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()

    def get_queryset(self):
        queryset = Attendance.objects.filter(session__subject__course__teacher = self.request.user)

        return queryset
    
    @action(detail=False, methods=["post"], url_path="bulk-create")
    def bulk_create (self, request):

        attendance_list = request.data.get("attendance", [])

        created = []
        for attendance in attendance_list:
            serializer = AttendanceSerializer(data=attendance)
            if serializer.is_valid():
                serializer.save()
                created.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(created, status=status.HTTP_201_CREATED)
