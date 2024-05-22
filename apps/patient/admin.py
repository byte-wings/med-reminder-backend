from django.contrib import admin
from .models import (
    Patient, ChronicCondition, PastSurgeryOrHospitalization, Allergy,
    CurrentMedication, FamilyMedicalHistory, LifestyleHabit,
    GeneralSymptom, RespiratorySymptom, CardiovascularSymptom,
    GastrointestinalSymptom, NeurologicalSymptom, MusculoskeletalSymptom,
    SkinSymptom
)

admin.site.register(Patient)
admin.site.register(ChronicCondition)
admin.site.register(PastSurgeryOrHospitalization)
admin.site.register(Allergy)
admin.site.register(CurrentMedication)
admin.site.register(FamilyMedicalHistory)
admin.site.register(LifestyleHabit)
admin.site.register(GeneralSymptom)
admin.site.register(RespiratorySymptom)
admin.site.register(CardiovascularSymptom)
admin.site.register(GastrointestinalSymptom)
admin.site.register(NeurologicalSymptom)
admin.site.register(MusculoskeletalSymptom)
admin.site.register(SkinSymptom)
