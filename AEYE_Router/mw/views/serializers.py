from rest_framework import serializers
from .models import aeye_inference_models, aeye_database__models


class aeye_inference_serializers(serializers.ModelSerializer):
    
    class Meta:
        model = aeye_inference_models
        fields = ['whoami', 'image', 'message']


class aeye__database_serializers(serializers.ModelSerializer):

    class Meta:
        model = aeye_database__models
        fields = ['whoami', 'message', 'operation', 'request_data']