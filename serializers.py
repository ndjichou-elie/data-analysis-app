from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class StockSymbolSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=10, required=True)
