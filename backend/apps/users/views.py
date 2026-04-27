from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny


from .models import Teacher
from .serializer import TeacherProfileSerializer, TeacherRegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherRegisterSerializer
    permission_classes = [AllowAny,]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        teacher = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not teacher.check_password(old_password):
            return Response({"error": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)

        teacher.set_password(new_password)
        teacher.save()
        return Response({"message": "Password updated"}, status=status.HTTP_200_OK)
