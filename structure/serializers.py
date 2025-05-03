from rest_framework import serializers
from .models import ServicesModel, StaticData
from main_.serializers import make_serializer_class


ServicesSer = make_serializer_class(ServicesModel)


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


