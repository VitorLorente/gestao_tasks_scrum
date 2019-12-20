from rest_framework import serializers
from core.models import (
    Sprint,
    Developer
)

class SprintSerializer(serializers.ModelSerializer):

    class Meta:

        model = Sprint
        fields = '__all__'


class DeveloperSerializer(serializers.ModelSerializer):

    class Meta:

        model = Developer
        fields = '__all__'


