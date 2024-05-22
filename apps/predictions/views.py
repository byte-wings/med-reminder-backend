import joblib
import pandas as pd
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .serializers import DiseasePredictionSerializer


class PredictDisease(GenericAPIView):
    serializer_class = DiseasePredictionSerializer
    model = joblib.load('research/disease_prediction_model.pkl')
    model_columns = joblib.load('research/model_columns.pkl')

    @staticmethod
    def translate_to_uzbek(text: str) -> str:
        translation_map = {
            "Healthy": "Sog'lom",
            "Diabetes": "Qandli diabet",
            "Thalasse": "Talassemiya",
            "Anemia": "Anemiya",
            "Thromboc": "Trombotsitoz"
        }
        return translation_map.get(text, "Sog'lom")  # Default to "Sog'lom" if not found

    @method_decorator(cache_page(60 * 15))
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            input_data = pd.DataFrame([serializer.validated_data])
            input_data.columns = [col.strip().lower().replace(' ', '_') for col in input_data.columns]

            # Ensure input_data columns match model_columns
            input_data = input_data.reindex(columns=self.model_columns, fill_value=0)

            prediction = self.model.predict(input_data)
            translated_prediction = self.translate_to_uzbek(prediction[0])
            return Response({'prediction': translated_prediction}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
