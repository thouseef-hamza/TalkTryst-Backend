from rest_framework import serializers
from .models import Account,Profile
from .helpers import send_otp_on_phone,verify_otp

class UserRegisterationSerializer(serializers.ModelSerializer):
    profile_picture=serializers.ImageField()
    class Meta:
        model=Account
        fields=("full_name","phone_number","profile_picture")
        
    def create(self, validated_data):
        otp=send_otp_on_phone(validated_data.get("phone_number"))
        if otp == "unavailable":
            raise serializers.ValidationError("Can't Process Your Request Now!")
        if otp == "invalid":
            raise serializers.ValidationError("Either this phone number is not valid or phone number is not registered on our service.Thank You!")
        user=Account.objects.create(
            full_name=validated_data.get("full_name"),
            phone_number=validated_data.get("phone_number"),
            verification_sid=otp
        )
        Profile.objects.create(
            user=user,
            profile_picture=validated_data.get("profile_picture")
        )
        return user
    
class OTPVerificationSerializer(serializers.Serializer):
    phone_number=serializers.CharField(max_length=15)
    otp=serializers.CharField(max_length=6)
    
    def validate(self, attrs):
        user=verify_otp(attrs["otp"],attrs["phone_number"])
        if user == 400:
            raise serializers.ValidationError("This user is already Exist! Try to login")
        return user
    
