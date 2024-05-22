from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChronicConditionViewSet, PastSurgeryOrHospitalizationViewSet, AllergyViewSet,
    CurrentMedicationViewSet, FamilyMedicalHistoryViewSet, LifestyleHabitViewSet, GeneralSymptomViewSet,
    RespiratorySymptomViewSet, CardiovascularSymptomViewSet, GastrointestinalSymptomViewSet,
    NeurologicalSymptomViewSet, MusculoskeletalSymptomViewSet, SkinSymptomViewSet
)

router = DefaultRouter()
router.register(r'chronic_conditions', ChronicConditionViewSet)
router.register(r'past_surgeries', PastSurgeryOrHospitalizationViewSet)
router.register(r'allergies', AllergyViewSet)
router.register(r'current_medications', CurrentMedicationViewSet)
router.register(r'family_histories', FamilyMedicalHistoryViewSet)
router.register(r'lifestyle_habits', LifestyleHabitViewSet)
router.register(r'general_symptoms', GeneralSymptomViewSet)
router.register(r'respiratory_symptoms', RespiratorySymptomViewSet)
router.register(r'cardiovascular_symptoms', CardiovascularSymptomViewSet)
router.register(r'gastrointestinal_symptoms', GastrointestinalSymptomViewSet)
router.register(r'neurological_symptoms', NeurologicalSymptomViewSet)
router.register(r'musculoskeletal_symptoms', MusculoskeletalSymptomViewSet)
router.register(r'skin_symptoms', SkinSymptomViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
