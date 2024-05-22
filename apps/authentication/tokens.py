from datetime import timedelta
from rest_framework_simplejwt.tokens import Token


class VerificationToken(Token):
    token_type = 'verification'
    lifetime = timedelta(minutes=1)  # Short-lived token for verification


class AuthenticationToken(Token):
    token_type = 'access'
    lifetime = timedelta(hours=2)  # Long-lived token for authenticated users
