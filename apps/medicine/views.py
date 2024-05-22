from rest_framework import viewsets

from .models import (
    ChronicCondition, PastSurgeryOrHospitalization, Allergy,
    CurrentMedication, FamilyMedicalHistory, LifestyleHabit, GeneralSymptom,
    RespiratorySymptom, CardiovascularSymptom, GastrointestinalSymptom,
    NeurologicalSymptom, MusculoskeletalSymptom, SkinSymptom
)
from apps.patient.serializers import dynamic_crud_serializer


class ChronicConditionViewSet(viewsets.ModelViewSet):
    queryset = ChronicCondition.objects.all()
    serializer_class = dynamic_crud_serializer(ChronicCondition, ['id', 'patient', 'condition', 'details'])


class PastSurgeryOrHospitalizationViewSet(viewsets.ModelViewSet):
    queryset = PastSurgeryOrHospitalization.objects.all()
    serializer_class = dynamic_crud_serializer(PastSurgeryOrHospitalization, ['id', 'patient', 'details', 'date'])


class AllergyViewSet(viewsets.ModelViewSet):
    queryset = Allergy.objects.all()
    serializer_class = dynamic_crud_serializer(Allergy, ['id', 'patient', 'allergy_type', 'details'])


class CurrentMedicationViewSet(viewsets.ModelViewSet):
    queryset = CurrentMedication.objects.all()
    serializer_class = dynamic_crud_serializer(CurrentMedication, ['id', 'patient', 'name', 'dosage', 'frequency'])


class FamilyMedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = FamilyMedicalHistory.objects.all()
    serializer_class = dynamic_crud_serializer(FamilyMedicalHistory, ['id', 'patient', 'relative', 'condition', 'details'])


class LifestyleHabitViewSet(viewsets.ModelViewSet):
    queryset = LifestyleHabit.objects.all()
    serializer_class = dynamic_crud_serializer(LifestyleHabit, ['id', 'patient', 'smoking_status', 'smoking_details', 'alcohol_consumption', 'alcohol_details', 'dietary_habits', 'physical_activity', 'sleep_patterns'])


class GeneralSymptomViewSet(viewsets.ModelViewSet):
    queryset = GeneralSymptom.objects.all()
    serializer_class = dynamic_crud_serializer(GeneralSymptom, ['id', 'patient', 'symptom', 'details'])


class RespiratorySymptomViewSet(viewsets.ModelViewSet):
    queryset = RespiratorySymptom.objects.all()
    serializer_class = dynamic_crud_serializer(RespiratorySymptom, ['id', 'patient', 'symptom', 'details'])


class CardiovascularSymptomViewSet(viewsets.ModelViewSet):
    queryset = CardiovascularSymptom.objects.all()
    serializer_class = dynamic_crud_serializer(CardiovascularSymptom, ['id', 'patient', 'symptom', 'details'])


class GastrointestinalSymptomViewSet(viewsets.ModelViewSet):
    queryset = GastrointestinalSymptom.objects.all()
    serializer_class = dynamic_crud_serializer(GastrointestinalSymptom, ['id', 'patient', 'symptom', 'details'])


class NeurologicalSymptomViewSet(viewsets.ModelViewSet):
    queryset = NeurologicalSymptom.objects.all()
    serializer_class = dynamic_crud_serializer(NeurologicalSymptom, ['id', 'patient', 'symptom', 'details'])


class MusculoskeletalSymptomViewSet(viewsets.ModelViewSet):
    queryset = MusculoskeletalSymptom.objects.all()
    serializer_class = dynamic_crud_serializer(MusculoskeletalSymptom, ['id', 'patient', 'symptom', 'details'])


class SkinSymptomViewSet(viewsets.ModelViewSet):
    queryset = SkinSymptom.objects.all()
    serializer_class = dynamic_crud_serializer(SkinSymptom, ['id', 'patient', 'symptom', 'details'])

