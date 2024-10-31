from rest_framework import serializers


class CategorySerializer(serializers.Serializer):

    # Explaining to Serializer: what model have, what type it is

    pk = serializers.IntegerField()
    name = serializers.CharField(required=True)
    kind = serializers.CharField()
    created_at = serializers.DateTimeField()
