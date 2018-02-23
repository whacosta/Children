from rest_framework import serializers
from .models import Nino
class NinoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Nino
        fields='__all__'