from rest_framework import serializers

from .models import Assessment, Grade

from apps.courses.models import Subject
from apps.courses.serializer import SubjectSerializer

from apps.students.models import Student
from apps.students.serializer import StudentSerializer

class AssessmentSerializer(serializers.ModelSerializer):

    subject = SubjectSerializer(read_only = True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset = Subject.objects.all(),
        source = 'subject',
        write_only = True
    )

    class Meta:
        model = Assessment
        fields = (
            "id",
            "subject",
            "subject_id",
            "name",
            "max_score",
            "date",
            "assessment_type"
        )


class GradeSerializer(serializers.ModelSerializer):

    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset = Student.objects.all(),
        source = "student",
        write_only = True
    )

    assessment = AssessmentSerializer(read_only = True)
    assessment_id = serializers.PrimaryKeyRelatedField(
        queryset = Assessment.objects.all(),
        source = 'assessment',
        write_only = True
    )

    class Meta:
        model = Grade
        fields = (
            "id",
            "student",
            "student_id",
            "assessment",
            "assessment_id",
            "score",
            "feedback",
        )