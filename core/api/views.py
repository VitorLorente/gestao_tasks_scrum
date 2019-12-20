from rest_framework import generics
from core.models import (
    Sprint,
    Developer
)
from .serializers import (
    SprintSerializer,
    DeveloperSerializer
)

# Create your views here.
class SprintApiList(generics.ListAPIView):

    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer


class DeveloperApiList(generics.ListAPIView):

    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer