from rest_framework import serializers
from .models import Account,Profile

class UserRegisterationSerializer(serializers.ModelSerializer):
    profile_picture=serializers.ImageField()
    class Meta:
        model=Account
        fields=("full_name","phone_number","otp","profile_picture")
        
    def create(self, validated_data):
        user=Account.objects.create(
            full_name=validated_data.get("full_name"),
            phone_number=validated_data.get("phone_number"),
            otp=validated_data.get("otp")
        )
        Profile.objects.create(
            user=user,
            profile_picture=validated_data.get("profile_picture")
        )
        
        