from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category  # give a model to serializer
        fields = "__all__"  # fields = ("name", "kind",) or exclude = ("created_at",)
