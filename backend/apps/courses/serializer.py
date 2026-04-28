from rest_framework import serializers

from .models import Subject, Course, Enrollment
from apps.students.serializer import StudentSerializer
from apps.students.models import Student

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "description",
            "weight",
            "course"
        )

class CourseSerializer(serializers.ModelSerializer):

    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "teacher",
            "subjects",
            "is_active",
        )
        read_only_fields = ("teacher",)

class EnrollmentSerializer(serializers.ModelSerializer):

    student = StudentSerializer(read_only=True)

    student_id = serializers.PrimaryKeyRelatedField(
        queryset = Student.objects.all(),
        source = 'student',
        write_only = True
    )

    course = CourseSerializer(read_only=True)

    course_id = serializers.PrimaryKeyRelatedField(
        queryset = Course.objects.all(),
        source = 'course',
        write_only = True
    )

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "student",
            "student_id",
            "course",
            "course_id",
            "date_enrolled",
            "status"
        )
        read_only_fields = ("date_enrolled",)

    
