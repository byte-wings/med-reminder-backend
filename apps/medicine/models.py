from django.db import models

from apps.patient.models import Patient

class ChronicCondition(models.Model):
    CONDITION_CHOICES = [
        ('diabetes', 'Diabetes'),
        ('hypertension', 'Hypertension'),
        ('heart_disease', 'Heart Disease'),
        ('asthma', 'Asthma'),
        ('copd', 'Chronic Obstructive Pulmonary Disease'),
        ('cancer', 'Cancer'),
        ('kidney_disease', 'Kidney Disease'),
        ('liver_disease', 'Liver Disease'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    details = models.TextField(blank=True, null=True)


class PastSurgeryOrHospitalization(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    details = models.TextField()
    date = models.DateField()


class Allergy(models.Model):
    ALLERGY_TYPE_CHOICES = [
        ('drug', 'Drug'),
        ('food', 'Food'),
        ('environmental', 'Environmental'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    allergy_type = models.CharField(max_length=50, choices=ALLERGY_TYPE_CHOICES)
    details = models.TextField()


class CurrentMedication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    frequency = models.CharField(max_length=255)


class FamilyMedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    relative = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)


class LifestyleHabit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    smoking_status = models.CharField(max_length=50)
    smoking_details = models.TextField(blank=True, null=True)
    alcohol_consumption = models.CharField(max_length=50)
    alcohol_details = models.TextField(blank=True, null=True)
    dietary_habits = models.TextField()
    physical_activity = models.TextField()
    sleep_patterns = models.TextField()


class GeneralSymptom(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptom = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)


class RespiratorySymptom(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptom = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)


class CardiovascularSymptom(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptom = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)


class GastrointestinalSymptom(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptom = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)


class NeurologicalSymptom(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptom = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)


class MusculoskeletalSymptom(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptom = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)


class SkinSymptom(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptom = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
