from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.models import User
from .models import UserConfirmation
from .serializers import (
    UserAuthSerializer,
    VerificationCodeSerializer,
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
        serializer = VerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            code = serializer.validated_data['code']
            try:
                payload = VerificationToken(token).payload
                user_id = payload['user_id']
                user = User.objects.get(id=user_id)
                self.check_verify(user, code)

                # User is now authenticated
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
            data = {
                'message': "Code is incorrect or expired"
            }
            user.delete()
            raise ValidationError(data)
        verifies.update(is_confirmed=True)
        user.save()
        return True


class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                return self.handle_request(serializer.validated_data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_request(self, data):
        token = data['refresh']
        token_type = data['token_type']

        if token_type == 'confirmation':
            return self.handle_confirmation(token)
        elif token_type == 'access':
            return super().post(self.request, *self.args, **self.kwargs)  # refresh access token using simplejwt
        else:
            return Response({"error": "Invalid token type."}, status=status.HTTP_400_BAD_REQUEST)

    def handle_confirmation(self, refresh_token: str):
        # user = generics.get_object_or_404(User, id=user_id)
        verification = UserConfirmation.objects.filter(
            user=user, code=code, is_confirmed=False, expiration_time__gte=timezone.now()
        ).first()

        if not verification:
            return Response({"error": "Invalid or expired code."}, status=status.HTTP_400_BAD_REQUEST)

        verification.is_confirmed = True
        verification.save()
        return self.generate_tokens(user)

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
            data = {
                "success": True,
                "message": "You are logged out"
            }
            return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
