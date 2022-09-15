from pyexpat import model
from rest_framework import serializers

from .models import ShipDetails

class CheckImoSerializer(serializers.ModelSerializer):
    class Meta:
        model= ShipDetails
        fields='__all__'
