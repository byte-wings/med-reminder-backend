from rest_framework import serializers


class DiseasePredictionSerializer(serializers.Serializer):
    glucose = serializers.FloatField(required=True)
    cholesterol = serializers.FloatField(required=True)
    hemoglobin = serializers.FloatField(required=True)
    platelets = serializers.FloatField(required=True)
    white_blood_cells = serializers.FloatField(required=True)
    red_blood_cells = serializers.FloatField(required=True)
    hematocrit = serializers.FloatField(required=True)
    mean_corpuscular_volume = serializers.FloatField(required=True)
    mean_corpuscular_hemoglobin = serializers.FloatField(required=True)
    mean_corpuscular_hemoglobin_concentration = serializers.FloatField(required=True)
    insulin = serializers.FloatField(required=False)  # Optional field
    bmi = serializers.FloatField(required=False)  # Optional field
    systolic_blood_pressure = serializers.FloatField(required=False)  # Optional field
    diastolic_blood_pressure = serializers.FloatField(required=False)  # Optional field
    triglycerides = serializers.FloatField(required=False)  # Optional field
    hba1c = serializers.FloatField(required=False)  # Optional field
    ldl_cholesterol = serializers.FloatField(required=False)  # Optional field
    hdl_cholesterol = serializers.FloatField(required=False)  # Optional field
    alt = serializers.FloatField(required=False)  # Optional field
    ast = serializers.FloatField(required=False)  # Optional field
    heart_rate = serializers.FloatField(required=False)  # Optional field
    creatinine = serializers.FloatField(required=False)  # Optional field
    troponin = serializers.FloatField(required=False)  # Optional field
    c_reactive_protein = serializers.FloatField(required=False)  # Optional field
