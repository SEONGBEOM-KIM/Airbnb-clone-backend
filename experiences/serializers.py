from rest_framework.serializers import ModelSerializer
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from .models import Perk, Experience


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = (
            "name",
            "detail",
            "explanation",
        )


class ExperienceSerializer(ModelSerializer):

    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    perks = PerkSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Experience
        exclude = (
            "created_at",
            "updated_at",
        )
