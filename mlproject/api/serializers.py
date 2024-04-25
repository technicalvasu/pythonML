from rest_framework import serializers
 
class InputSerializer(serializers.Serializer):
    source = serializers.CharField(max_length=100)
    numberOfLineItem = serializers.IntegerField()
    totalQuantity = serializers.IntegerField()
 
class OutputSerializer(serializers.Serializer):
    source = serializers.CharField()
    score = serializers.IntegerField()
    timePredicted = serializers.FloatField()