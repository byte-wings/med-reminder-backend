from rest_framework import generics, permissions
from .serializers import UserSerializer, UserUpdateSerializer

from .models import User


class UserDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve the authenticated user's details.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    """
    API endpoint to update the authenticated user's details.
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
