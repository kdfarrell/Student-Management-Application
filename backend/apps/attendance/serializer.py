from rest_framework import serializers

from .models import Attendance
from apps.students.models import Student
from apps.scheduling.models import ClassSession

from apps.students.serializer import StudentSerializer
from apps.scheduling.serializer import ClassSessionSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    
    student = StudentSerializer(read_only = True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset = Student.objects.all(),
        source = "student",
        write_only = True
    )

    session = ClassSessionSerializer(read_only=True)
    session_id = serializers.PrimaryKeyRelatedField(
        queryset = ClassSession.objects.all(),
        source = "session",
        write_only = True,
    )

    class Meta:
        model = Attendance 
        fields = (
            "id",
            "student",
            "student_id",
            "session",
            "session_id",
            "status",
            "notes"
        )