from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(
        "users.Teacher",
        on_delete=models.CASCADE,
        related_name="courses"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ("name", "teacher")
        ordering = ['name']


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        related_name="subjects"
    )

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ("name", "course")
        ordering = ["id"]


class Enrollment(models.Model):
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        related_name="enrolled_students"
    )

    date_enrolled = models.DateField(auto_now_add=True)

    STATUS_CHOICES = [ ("active", "Active"), ("dropped", "Dropped"), ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    class Meta:
        unique_together = ("course", "student")

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name}: {self.course.name}"
    
    
