from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterationSerializer,OTPVerificationSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework import status

# Create your views here.


class UserRegistrationAPIView(APIView):
    parser_classes=(MultiPartParser,)
    def post(self,request):
        serializer=UserRegisterationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

class OTPVerificationAPIView(APIView):
    def post(self,request):
        serializer=OTPVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)