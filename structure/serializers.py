from rest_framework import serializers
from .models import ServicesModel, StaticData, H_Vac_CategoryModel, BannersModel, BlogsModel, OurClientsModel, \
    ProductModel, CapacityModel, CategoryGeneratorSet, ProductGeneratorSet, FireProductsModel, BrandGeneratorSetModel, \
    BrandsModel, ContactUsModel, ClientKindModel, ContactKindModel
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


class BrandsSer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True, source="products.count")

    class Meta:
        model = BrandsModel
        fields = "__all__"


class CapacitySer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True, source="products.count")

    class Meta:
        model = CapacityModel
        fields = "__all__"


class ProductSer(serializers.ModelSerializer):
    brand_info = BrandsSer(read_only=True, source="brand")
    capacity_info = CapacitySer(read_only=True, source="capacity")

    class Meta:
        model = ProductModel
        fields = "__all__"


ProductMiniSer = make_serializer_class(ProductModel, "id", "name_ar", "name_en")

BlogsSer = make_serializer_class(BlogsModel)
BlogsMiniSer = make_serializer_class(BlogsModel, "id", "name_ar", "name_en")

OurClientsSer = make_serializer_class(OurClientsModel)


class CategoryGeneratorSer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True, source="products.count")

    class Meta:
        model = CategoryGeneratorSet
        fields = "__all__"


class BrandGeneratorSetSer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True, source="products.count")

    class Meta:
        model = BrandGeneratorSetModel
        fields = "__all__"


class ProductGeneratorSetSer(serializers.ModelSerializer):
    category_info = CategoryGeneratorSer(read_only=True, source="category")
    brand_info = BrandGeneratorSetSer(read_only=True, source="brand")
    products_info = ProductMiniSer(read_only=True, source="products", many=True)

    class Meta:
        model = ProductGeneratorSet
        fields = "__all__"


ProductGeneratorMiniSetSer = make_serializer_class(ProductGeneratorSet, "id", "name_ar", "name_en")
ClientKindSer = make_serializer_class(ClientKindModel)
FireProductsSer = make_serializer_class(FireProductsModel)
FireProductsMiniSer = make_serializer_class(FireProductsModel, "id", "name_ar", "name_en")
ContactKindModelSer = make_serializer_class(ContactKindModel)


class ContactUsModelSer(serializers.ModelSerializer):
    kind = serializers.SlugRelatedField(
        queryset=ContactKindModel.objects.all(),
        slug_field='kind'  # الحقل اللي هتشتغل عليه (الـ Name)
    )
    product_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ContactUsModel
        fields = "__all__"

    def get_product_info(self, obj):
        if obj.product:
            return ProductSer(obj.product).data
        elif obj.product_generator_set:
            return ProductGeneratorSetSer(obj.product_generator_set).data
        elif obj.product_fire:
            return FireProductsSer(obj.product_fire).data

        return None


class ClintKindDetailsSer(serializers.ModelSerializer):
    clients = OurClientsSer(many=True, read_only=True)

    class Meta:
        model = ClientKindModel
        fields = "__all__"
