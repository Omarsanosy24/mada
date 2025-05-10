from main_.permissions import HasAPIKeyWithTimeCheck
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

from main_.viewset import ModelViewSetIndividual
from .models import StaticData, H_Vac_CategoryModel, BannersModel, BlogsModel, OurClientsModel, ProductModel, \
    CapacityModel, ProductGeneratorSet, CategoryGeneratorSet, FireProductsModel
from .serializers import StaticDataSer, H_Vac_CategorySer, BannersSer, BlogsSer, OurClientsSer, ProductSer, \
    CapacitySer, ProductGeneratorSetSer, CategoryGeneratorSer, FireProductsSer


class StaticDataViewSet(ModelViewSetIndividual):
    queryset = StaticData.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = StaticDataSer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["kind", 'place']
    lookup_field = "kind"


class H_Vac_CategoryViewSet(ModelViewSetIndividual):
    queryset = H_Vac_CategoryModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = H_Vac_CategorySer
    filter_backends = [DjangoFilterBackend]


class BannersView(ModelViewSetIndividual):
    queryset = BannersModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = BannersSer
    filter_backends = [DjangoFilterBackend]


class BlogsView(ModelViewSetIndividual):
    queryset = BlogsModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = BlogsSer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["kind"]


class OurClientsView(ModelViewSetIndividual):
    queryset = OurClientsModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = OurClientsSer
    filter_backends = [DjangoFilterBackend]


class ProductView(ModelViewSetIndividual):
    queryset = ProductModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = ProductSer
    filter_backends = [DjangoFilterBackend]


class CapacityView(ModelViewSetIndividual):
    queryset = CapacityModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = CapacitySer
    filter_backends = [DjangoFilterBackend]


class CategoryGeneratorViewSet(ModelViewSetIndividual):
    queryset = CategoryGeneratorSet.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = CategoryGeneratorSer
    filter_backends = [DjangoFilterBackend]


class ProductGeneratorSetViewSet(ModelViewSetIndividual):
    queryset = ProductGeneratorSet.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = ProductGeneratorSetSer
    filter_backends = [DjangoFilterBackend]


class FireProductsViewSet(ModelViewSetIndividual):
    queryset = FireProductsModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = FireProductsSer
    filter_backends = [DjangoFilterBackend]
