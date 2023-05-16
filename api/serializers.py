from rest_framework import serializers
from core.models import Exercise
from Workshops.models import Workshop

class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = "__all__"

class BodyPartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = ["bodyPart"]

class WorkshopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workshop
        fields="__all__"


