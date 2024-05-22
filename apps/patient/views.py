from rest_framework import viewsets

from .models import Patient
from .serializers import dynamic_crud_serializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = dynamic_crud_serializer(Patient, ['id', 'user', 'height', 'weight', 'ethnicity'])
