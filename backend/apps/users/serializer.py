from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Teacher

# For creating a teacher 
class TeacherRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ['username', 'password', 'email', 'school_name']
        model = Teacher

    def create(self, validated_data):
        password = validated_data.pop("password")

        teacher = Teacher(**validated_data)
        teacher.set_password(password)
        teacher.save()

        return teacher
    
    
# For viewing and updating 
class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'email', 'school_name']
        model = Teacher


class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['school_name'] = user.school_name
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['school_name'] = self.user.school_name
        return data
    
