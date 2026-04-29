from rest_framework import serializers

from .models import ClassSession

class ClassSessionSerializer(serializers.ModelSerializer):
    
    course_name = serializers.CharField(source="subject.course.name", read_only=True)

    subject_name = serializers.CharField(source="subject.name", read_only=True)

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
        )