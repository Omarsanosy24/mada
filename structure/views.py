from main_.permissions import HasAPIKeyWithTimeCheck
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

from main_.viewset import ModelViewSetIndividual
from .models import ServicesModel, StaticData
from .serializers import StaticDataSer


class StaticDataViewSet(ModelViewSetIndividual):
    queryset = StaticData.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = StaticDataSer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["kind", 'place']


