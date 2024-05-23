from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.models import User
from .models import UserConfirmation, ConfirmationRefreshToken
from .serializers import (
    UserAuthSerializer,
    VerificationCodeSerializer,
    CustomRefreshTokenSerializer,
    LogoutSerializer
)
from apps.authentication.tokens import AuthenticationToken, VerificationToken


class UserAuthView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response = Response({
                "access_token": serializer.validated_data["access_token"],
                "is_new": serializer.validated_data["is_new"],
            })
            response.set_cookie(
                key="refresh_token",
                value=serializer.validated_data["refresh_token"],
                httponly=True,
                secure=True,  # Use True if using HTTPS
                samesite='Strict'
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerificationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            code = serializer.validated_data['code']
            try:
                payload = VerificationToken(token).payload
                user_id = payload['user_id']
                user = User.objects.get(id=user_id)
                self.check_verify(user, code)
                access_token = AuthenticationToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)
                response = Response({
                    "access_token": str(access_token),
                }, status=status.HTTP_200_OK)
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh_token),
                    httponly=True,
                    secure=True,  # Use True if using HTTPS
                    samesite='Strict'
                )
                return response
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(
            expiration_time__gte=timezone.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            user.delete()
            raise ValidationError({'message': "Code is incorrect or expired"})
        verifies.update(is_confirmed=True)
        user.save()
        return True


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomRefreshTokenSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                return self.handle_request(serializer.validated_data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_request(self, data):
        refresh_token = data['refresh']
        token_type = data['token_type']

        if token_type == 'confirmation':
            return self.handle_confirmation(refresh_token)
        elif token_type == 'access':
            return super().post(self.request, *self.args, **self.kwargs)  # refresh access token using simplejwt
        return Response({"error": "Invalid token type."}, status=status.HTTP_400_BAD_REQUEST)

    def handle_confirmation(self, refresh_token):
        try:
            # Decode the refresh token to get the user information
            token = RefreshToken(refresh_token)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)

            # Retrieve the ConfirmationRefreshToken
            confirmation_token = ConfirmationRefreshToken.objects.get(user=user, token=refresh_token)

            # Check if the refresh count is within the limit
            if not confirmation_token.is_refreshable():
                return Response({"error": "Refresh token usage limit exceeded."}, status=status.HTTP_400_BAD_REQUEST)

            # Update the refresh count and save the token
            confirmation_token.refresh_count += 1
            confirmation_token.save()

            # Generate a new access token and a new verification code
            access_token = VerificationToken.for_user(user)
            verification_code = user.create_verify_code()

            response_data = {
                "access_token": str(access_token),
                "verification_code": verification_code,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except ConfirmationRefreshToken.DoesNotExist:
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def generate_tokens(self, user):
        access_token = VerificationToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        response_data = {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
        }
        response = Response(response_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key='confirmation_refresh_token',
            value=str(refresh_token),
            httponly=True,
            secure=True,  # Use True if using HTTPS
            samesite='Strict'
        )
        return response


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": True, "message": "You are logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
