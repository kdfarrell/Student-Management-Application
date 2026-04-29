from django.db import models

class ClassSession(models.Model):
    subject = models.ForeignKey(
        "courses.Subject",
        on_delete=models.CASCADE,
        related_name="class_sessions"
    )

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    room = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    @property
    def teacher(self):
        return self.subject.course.teacher
    
    class Meta:
        unique_together = ("subject", "date", "start_time")