from django.db import models
from rest_framework import serializers

from .models import Drugs, MedicationSchedule


def dynamic_crud_serializer(model: models.Model, fields: list, update=True):
    """
    Function to create a dynamically generated serializer for CRUD operations.

    Args:
        model (models.Model): The Django model for which the serializer is generated.
        fields (list): List of fields to be included in the serializer.
        update (bool, optional): Whether the serializer should include the primary key field for update operations. Defaults to True.

    Returns:
        serializers.ModelSerializer: The generated serializer class.
    """

    class DynamicCRUDSerializer(serializers.ModelSerializer):
        def __init__(self, *args, **kwargs):
            super(DynamicCRUDSerializer, self).__init__(*args, **kwargs)

            if update:
                pk_field = self.Meta.model._meta.pk.name
                self.fields[pk_field] = serializers.PrimaryKeyRelatedField(
                    queryset=self.Meta.model.objects.all(),
                    required=True,
                )

            for field_name, field in self.fields.items():
                field.required = True

        class Meta:
            model = None
            fields = None

    DynamicCRUDSerializer.Meta.model = model
    DynamicCRUDSerializer.Meta.fields = fields

    return DynamicCRUDSerializer


class MedicationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationSchedule
        fields = ['weekday', 'time']


class DrugSerializer(serializers.ModelSerializer):
    schedule = MedicationScheduleSerializer(many=True)

    class Meta:
        model = Drugs
        fields = ['type', 'amount', 'dose', 'notes', 'schedule']

    def create(self, validated_data):
        schedule_data = validated_data.pop('schedule')
        request = self.context['request']
        patient = request.user  # Get the authenticated user

        drug = Drugs.objects.create(patient=patient, **validated_data)
        for schedule in schedule_data:
            MedicationSchedule.objects.create(drug=drug, **schedule)
        return drug
