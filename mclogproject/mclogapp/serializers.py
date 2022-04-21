from rest_framework import serializers

from .models import ShipDetails

class CheckImoSerializer(serializers.Serializer):
    class Meta:
        model= ShipDetails
        fields=['shipImo']