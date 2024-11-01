from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category  # give a model to serializer
        fields = (
            "name",
            "kind",
        )  # f "__all__" / exclude = ("created_at",)
