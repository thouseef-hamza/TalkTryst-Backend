from twilio.rest import Client
from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from .models import Account
from rest_framework.exceptions import NotFound,AuthenticationFailed

# def send_otp_sms(phone_number):
#     otp=requests.get(f"https://2factor.in/API/V1/{settings.SMS_API_KEY}/SMS/+91{phone_number}/1234/Talk+Tryst")
#     print(otp.status_code)

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_otp_on_phone(phone_number):
    try:
        verification = client.verify.v2.services(
            settings.TWILIO_SERVICE_SID
        ).verifications.create(to=phone_number, channel="sms")
        return verification.sid
    except TwilioRestException as e:
        return "invalid"
    except ConnectionError as e:
        return "unavailable"

def verify_otp(otp,phone_number):
    try:
        user=Account.objects.get(phone_number=phone_number)
    except Account.DoesNotExist:
        raise NotFound("User with this Account Not Found")
    if not user.is_active:
        try:
            verification_check = client.verify.v2.services(
                settings.TWILIO_SERVICE_SID
            ).verification_checks.create(
                verification_sid=user.verification_sid, code=otp
            )

        except TwilioRestException as e:
            raise e
        if verification_check.status == "approved":
            user.is_active = True
            return user
        elif verification_check.status == "pending":
            raise AuthenticationFailed("Your Request Has Been Validating")
        else:
            raise AuthenticationFailed("Please Check Your OTP")
    else:
        return 400
