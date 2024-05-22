from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .utils import phone_parser
from apps.user.models import User
from .tokens import VerificationToken
from config.utility import check_phone
from .models import ConfirmationRefreshToken


class UserAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=16)

    def validate_phone_number(self, phone_number):
        if check_phone(phone_number):
            phone_parser(phone_number, self.initial_data.get('country'))
        else:
            data = {
                "success": False,
                'message': "Your phone number is incorrect"
            }
            raise ValidationError(data)
        return phone_number

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        user = self.get_or_create_user(phone_number)

        access_token = VerificationToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        ConfirmationRefreshToken.objects.update_or_create(user=user, defaults={'token': str(refresh_token)})
        return {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token)
        }

    @staticmethod
    def get_or_create_user(phone_number: str) -> User:
        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            user.set_unusable_password()
            user.save()
        code = user.create_verify_code()
        # send_phone_notification.delay(user.phone_number, code)
        print(code)
        return user


class VerificationCodeSerializer(serializers.Serializer):
    token = serializers.CharField()
    code = serializers.CharField(required=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        help_text="The refresh token obtained during login.",
        label="Refresh Token",
        required=True
    )
