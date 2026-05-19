from django.db import models


class Assessment(models.Model):
    subject = models.ForeignKey(
        "courses.Subject",
        on_delete=models.CASCADE,
        related_name="assessments"
    )

    name = models.CharField(max_length=200)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()

    ASSESSMENT_CHOICES = [
        ("test", "Test"),
        ("assignment", "Assignment"),
        ("exam", "Exam"),
        ("quiz", "Quiz"),
    ]

    assessment_type = models.CharField(
        max_length=15,
        choices=ASSESSMENT_CHOICES,
        default="exam"
    )

    class Meta:
        ordering = ['date', 'name']        
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Grade(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="grades"
    )

    assessment = models.ForeignKey(
        "Assessment",
        on_delete=models.CASCADE,
        related_name="grades"
    )

    score = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ("student", "assessment")
        ordering = ['assessment__date', 'student__last_name', 'student__first_name']
        verbose_name = "Grade"
        verbose_name_plural = "Grades"

    def __str__(self):
        return f"{self.student}: {self.assessment}"