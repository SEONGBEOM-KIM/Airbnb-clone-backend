from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated
from categories.models import Category
from .serializers import PerkSerializer, ExperienceSerializer
from .models import Perk, Experience


class Perks(APIView):

    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(
            all_perks,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Experiences(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceSerializer(
            all_experiences,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:  # <- category not in request
                raise ParseError("Category is required")
            try:  # <- have category in request
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The Category kind should be 'experience'")
            except Category.DoesNotExist:  # <- user give wrong category with db
                raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
                    serializer = ExperienceSerializer(
                        experience,
                        context={"request": request},
                    )
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Perk not found")
        else:
            return Response(serializer.errors)
