from django.contrib import admin

from .models import Course, Subject, Enrollment

admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Enrollment)
