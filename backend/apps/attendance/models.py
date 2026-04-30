from django.db import models

class Attendance(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="attendance"
    )

    session = models.ForeignKey(
        "scheduling.ClassSession",
        on_delete=models.CASCADE,
        related_name="attendance"
    )

    STATUS_CHOICES = [
        ("present", "Present"),
        ("late", "Late"),
        ("absent", "Absent"),
        ("excused", "Excused"),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default="present"
    )

    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("student", "session")

    def __str__(self):
        return f"{self.student} - {self.session} - {self.status}"
