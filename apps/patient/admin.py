from django.contrib import admin
from .models import Patient, Appointment, Drugs, MedicationSchedule

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Drugs)
admin.site.register(MedicationSchedule)
