from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(
        "users.Teacher",
        on_delete=models.CASCADE,
        related_name='students'
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"