from rest_framework import serializers
from .models import ServicesModel, StaticData, H_Vac_CategoryModel, BannersModel, BlogsModel, OurClientsModel, \
    ProductModel, CapacityModel, CategoryGeneratorSet, ProductGeneratorSet, FireProductsModel, BrandGeneratorSetModel, \
    BrandsModel
from main_.serializers import make_serializer_class

ServicesSer = make_serializer_class(ServicesModel)
H_Vac_CategorySer = make_serializer_class(H_Vac_CategoryModel)


class StaticDataSer(serializers.ModelSerializer):
    services = ServicesSer(many=True, read_only=True)
    create_services = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )

    class Meta:
        model = StaticData
        fields = "__all__"

    def create(self, validated_data):
        services = validated_data.pop("create_services")
        static_data = super().create(validated_data)
        for service in services:
            ServicesModel.objects.create(static_data=static_data, **service)
        return static_data


BannersSer = make_serializer_class(BannersModel)
BrandsSer = make_serializer_class(BrandsModel)
CapacitySer = make_serializer_class(CapacityModel)


class ProductSer(serializers.ModelSerializer):
    brand_info = BrandsSer(read_only=True)
    capacity_info = CapacitySer(read_only=True)

    class Meta:
        model = ProductModel
        fields = "__all__"


ProductMiniSer = make_serializer_class(ProductModel, "id", "name_ar", "name_en")

BlogsSer = make_serializer_class(BlogsModel)
BlogsMiniSer = make_serializer_class(BlogsModel, "id", "name_ar", "name_en")

OurClientsSer = make_serializer_class(OurClientsModel)

CategoryGeneratorSer = make_serializer_class(CategoryGeneratorSet)
BrandGeneratorSetSer = make_serializer_class(BrandGeneratorSetModel)


class ProductGeneratorSetSer(serializers.ModelSerializer):
    category_info = CategoryGeneratorSer(read_only=True)
    product_info = BrandGeneratorSetSer(read_only=True)

    class Meta:
        model = ProductGeneratorSet
        fields = "__all__"


FireProductsSer = make_serializer_class(FireProductsModel)
