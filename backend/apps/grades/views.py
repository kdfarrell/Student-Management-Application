from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from collections import defaultdict

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Assessment, Grade
from .serializer import AssessmentSerializer, GradeSerializer

from apps.students.models import Student 

from apps.audit.utils import log_audit


class AssessmentViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AssessmentSerializer
    queryset = Assessment.objects.all()

    def get_queryset(self):
        queryset = Assessment.objects.filter(subject__course__teacher = self.request.user)

        return queryset

class GradeViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()

    def get_queryset(self):
        queryset = Grade.objects.filter(assessment__subject__course__teacher = self.request.user)


        return queryset
    
    @action(detail=False, methods=['get'], url_path="student-report")
    def student_report(self, request):
        student_id = request.query_params.get("student_id")
        student = get_object_or_404(Student, pk=student_id)

        grades = Grade.objects.filter(student = student, assessment__subject__course__teacher = self.request.user)

        subject_grades = defaultdict(list)
        for grade in grades:
            subject = grade.assessment.subject
            subject_grades[subject].append(grade)

        report = []

        for subject, subject_grade_list in subject_grades.items():
            total_weighted = 0
            total_weight = 0

            for grade in subject_grade_list:
                total_weighted += (grade.score / grade.assessment.max_score) * subject.weight
                total_weight += subject.weight

            weighted_average = total_weighted / total_weight if total_weight > 0 else 0

            report.append({
                "subject": subject.name,
                "weight": subject.weight,
                "weighted_average": round(weighted_average * 100, 2)
            })
        
        return Response(report)

    def perform_create(self, serializer):
        grade = serializer.save()
        log_audit(
            teacher=self.request.user,
            action='create',
            target_model = "Grade",
            target_id = grade.id,
            detail={"score": str(grade.score), "feedback": grade.feedback}
        )

    def perform_update(self, serializer):
        old_score = serializer.instance.score
        grade = serializer.save()

        log_audit(
            teacher=self.request.user,
            action="update",
            target_model = "Grade",
            target_id = grade.id,
            detail = {"before": str(old_score), "after":str(grade.score)}
        )

