from django.db import models

class Audit(models.Model):
    teacher = models.ForeignKey(
        "users.Teacher",
        on_delete=models.CASCADE,
        related_name="audits"
    )

    action = models.CharField(max_length=100)
    target_model = models.CharField(max_length = 100)
    target_id = models.IntegerField()
    detail = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher}: {self.action}\nModel: {self.target_model}"