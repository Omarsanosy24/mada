import django_filters
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from main_.permissions import HasAPIKeyWithTimeCheck
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

from main_.viewset import ModelViewSetIndividual
from .models import StaticData, H_Vac_CategoryModel, BannersModel, BlogsModel, OurClientsModel, ProductModel, \
    CapacityModel, ProductGeneratorSet, CategoryGeneratorSet, FireProductsModel, BrandsModel, BrandGeneratorSetModel, \
    ContactUsModel, ContactKindModel, ClientKindModel
from .serializers import StaticDataSer, H_Vac_CategorySer, BannersSer, BlogsSer, OurClientsSer, ProductSer, \
    CapacitySer, ProductGeneratorSetSer, CategoryGeneratorSer, FireProductsSer, BrandsSer, BrandGeneratorSetSer, \
    ContactUsModelSer, ContactKindModelSer, ClientKindSer, ClintKindDetailsSer, ProductGeneratorMiniSetSer, \
    FireProductsMiniSer, BlogsMiniSer, ProductMiniSer


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
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["id"]


class BannersView(ModelViewSetIndividual):
    queryset = BannersModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = BannersSer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["id"]


class BlogsView(ModelViewSetIndividual):
    queryset = BlogsModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = BlogsSer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["kind"]

    def get_serializer_class(self):
        if "mini" in self.request.query_params:
            return BlogsMiniSer
        return super().get_serializer_class()


class OurClientsView(ModelViewSetIndividual):
    queryset = OurClientsModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = OurClientsSer
    filter_backends = [DjangoFilterBackend]


class ProductFilter(django_filters.FilterSet):
    brand = django_filters.ModelMultipleChoiceFilter(
        field_name="brand",
        queryset=BrandsModel.objects.all(),
        to_field_name="id",
    )
    capacity = django_filters.ModelMultipleChoiceFilter(
        field_name="capacity",
        queryset=CapacityModel.objects.all(),
        to_field_name="id",
    )


class ProductView(ModelViewSetIndividual):
    queryset = ProductModel.objects.select_related("brand", "capacity").all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = ProductSer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if "mini" in self.request.query_params:
            return ProductMiniSer
        return super().get_serializer_class()


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


class ProductGeneratorSetFilter(django_filters.FilterSet):
    brand = django_filters.ModelMultipleChoiceFilter(
        field_name="brand",
        queryset=BrandsModel.objects.all(),
        to_field_name="id",
    )
    category = django_filters.ModelMultipleChoiceFilter(
        field_name="category",
        queryset=CategoryGeneratorSet.objects.all(),
        to_field_name="id",
    )


class ProductGeneratorSetViewSet(ModelViewSetIndividual):
    queryset = ProductGeneratorSet.objects.select_related("brand", "category").all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = ProductGeneratorSetSer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductGeneratorSetFilter

    def get_serializer_class(self):
        if "mini" in self.request.query_params:
            return ProductGeneratorMiniSetSer
        return super().get_serializer_class()


class FireProductsViewSet(ModelViewSetIndividual):
    queryset = FireProductsModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = FireProductsSer
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if "mini" in self.request.query_params:
            return FireProductsMiniSer
        return super().get_serializer_class()


class BrandGeneratorSetViewSet(ModelViewSetIndividual):
    queryset = BrandGeneratorSetModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = BrandGeneratorSetSer
    filter_backends = [DjangoFilterBackend]


class BrandsViewSet(ModelViewSetIndividual):
    queryset = BrandsModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = BrandsSer
    filter_backends = [DjangoFilterBackend]


class ContactUsModelViewSet(ModelViewSetIndividual):
    queryset = ContactUsModel.objects.all()
    permission_classes = [HasAPIKeyWithTimeCheck]
    serializer_class = ContactUsModelSer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["kind__kind"]


class ContactKindModelViewSet(ModelViewSetIndividual):
    queryset = ContactKindModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = ContactKindModelSer
    lookup_field = "kind"


class ClientKindModelViewSet(ModelViewSetIndividual):
    queryset = ClientKindModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, HasAPIKeyWithTimeCheck]
    serializer_class = ClientKindSer
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if "client" in self.request.query_params:
            return ClintKindDetailsSer
        return super().get_serializer_class()


class NumOfPageForAllProductsView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        import math
        try:
            limit = int(request.query_params.get("page_limit", 10))
        except ValueError:
            limit = 10
        return Response(
            {
                "blogs": math.ceil(BlogsModel.objects.count() / limit) + 1,
                "product": math.ceil(ProductModel.objects.count() / limit) + 1,
                "product_generator_set": math.ceil(ProductGeneratorSet.objects.count() / limit) + 1,
                "product_fire": math.ceil(FireProductsModel.objects.count() / limit) + 1,
            }
        )
