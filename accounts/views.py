from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterationSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework import status
# Create your views here.


class UserRegistrationAPIView(APIView):
    parser_classes=(MultiPartParser,)
    def post(self,request):
        serializer=UserRegisterationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        user=serializer.save()
        return Response({"OTP":user.otp},status=status.HTTP_201_CREATED)
