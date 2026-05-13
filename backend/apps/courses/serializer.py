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


class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course_name = serializers.ReadOnlyField(source='course.name')
    
    course_is_active = serializers.ReadOnlyField(source='course.is_active')

    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        source='student',
        write_only=True
    )
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source='course',
        write_only=True
    )

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "student",
            "course_name",
            "course_is_active", 
            "student_id",
            "course_id",
            "date_enrolled",
            "status"
        )
        read_only_fields = ("date_enrolled",)
class CourseSerializer(serializers.ModelSerializer):

    subjects = SubjectSerializer(many=True, read_only=True)
    enrolled_students_count = serializers.IntegerField(
        source='enrolled_students.count',
        read_only=True
    )

    enrolled_students_count = serializers.SerializerMethodField()

    def get_enrolled_students_count(self, obj):
        return obj.enrolled_students.filter(status='active').count()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "teacher",
            "subjects",
            "enrolled_students_count",
            "is_active",
        )
        read_only_fields = ("teacher",)