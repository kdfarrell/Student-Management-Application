from rest_framework import serializers

from .models import Audit
from apps.users.models import Teacher
from apps.users.serializer import TeacherProfileSerializer

class AuditSerializer(serializers.ModelSerializer):

    teacher = TeacherProfileSerializer(read_only=True)

    class Meta:
        model = Audit
        fields = (
            "id",
            "teacher",
            "action",
            "target_model",
            "target_id",
            "detail",
            "timestamp"
        )