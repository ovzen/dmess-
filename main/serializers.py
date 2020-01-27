from rest_framework import serializers


class DialogSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    create_date = serializers.DateTimeField()
    last_change = serializers.DateTimeField()
    # users = serializers.