from rest_framework.response import Response
from rest_framework import viewsets, status, permissions

from .models import Patient, Drugs
from .serializers import dynamic_crud_serializer, DrugSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = dynamic_crud_serializer(Patient, ['id', 'user', 'height', 'weight', 'ethnicity'])


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drugs.objects.all()
    serializer_class = DrugSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        # Return only the drugs for the authenticated user
        return self.queryset.filter(patient=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
