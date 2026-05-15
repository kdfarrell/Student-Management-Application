from rest_framework import serializers

from .models import ClassSession
# --- IMPORT REQUIRED FOR THE CHECK ---
from apps.attendance.models import Attendance  # <-- Adjust this path if your attendance model is located elsewhere!

class ClassSessionSerializer(serializers.ModelSerializer):
    
    course_name = serializers.CharField(source="subject.course.name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    
    # 1. Declare our calculated boolean property field
    attendance_recorded = serializers.SerializerMethodField()

    class Meta:
        model = ClassSession
        fields = (
            "id",
            "date",
            "start_time",
            "end_time",
            "room",
            "course_name",
            "subject",
            "subject_name",
            "notes",
            "attendance_recorded", # 2. Append the new field key to your exposure tuple
        )

    # 3. Add the evaluation logic method
    def get_attendance_recorded(self, obj):
        # Scans the database table to see if any rows match this ClassSession instance
        return Attendance.objects.filter(session=obj).exists()