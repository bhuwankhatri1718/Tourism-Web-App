from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from .models import TouristProfile
from .serializers import RegisterSerializer, TouristProfileSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'message': 'Registration successful', 'username': user.username},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TouristProfileView(RetrieveUpdateAPIView):
    serializer_class = TouristProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return TouristProfile.objects.get(user=self.request.user)