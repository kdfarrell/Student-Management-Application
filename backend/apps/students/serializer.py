from rest_framework import serializers

from .models import Student 

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student 
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "date_of_birth",
            "teacher",
            "enrollment_date",
            "is_active",
        )
        read_only_fields = ("teacher", "enrollment_date")