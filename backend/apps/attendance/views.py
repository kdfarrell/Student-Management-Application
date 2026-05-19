from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.audit.utils import log_audit

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
    def bulk_create(self, request):
        attendance_list = request.data.get("attendance", [])
        created_or_updated = []
        
        # Track the session ID so we can flag it as recorded
        session_id = None

        for attendance_data in attendance_list:
            student_id = attendance_data.get("student_id")
            session_id = attendance_data.get("session_id")
            status_value = attendance_data.get("status")
            notes_value = attendance_data.get("notes", "")

            instance = Attendance.objects.filter(student_id=student_id, session_id=session_id).first()

            if instance:
                serializer = AttendanceSerializer(instance, data=attendance_data, partial=True)
            else:
                serializer = AttendanceSerializer(data=attendance_data)

            if serializer.is_valid():
                serializer.save()
                created_or_updated.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        # --- CRITICAL BADGE UPDATE FIX ---
        # If we successfully processed records, update the parent session flag
        if session_id and created_or_updated:
            from apps.scheduling.models import ClassSession
            ClassSession.objects.filter(id=session_id).update(attendance_recorded=True)
            log_audit(
                teacher=request.user,
                action="update",
                target_model="Attendance",
                target_id=session_id,
                detail={
                    "session_id": session_id,
                    "records_saved": len(created_or_updated),
                },
            )

        return Response(created_or_updated, status=status.HTTP_201_CREATED)