from rest_framework.serializers import ModelSerializer


class CustomModelSerializer(ModelSerializer):
    def get_fields(self):
        fields = super().get_fields()
        fields = self.remove_fields(fields)
        fields = self.custom_only_fileds(fields)
        return fields

    def custom_only_fileds(self, fields):
        if hasattr(self.Meta, 'custom_fields_query') and self.context.get('request', False):
            if self.Meta.custom_fields_query in self.context['request'].query_params:
                keys = list(fields.keys())
                for f in keys:
                    if f not in self.context['request'].query_params[self.Meta.custom_fields_query].split(","):
                        fields.pop(f)
        return fields

    def remove_fields(self, fields):
        if hasattr(self.Meta, 'removed_fields_query') and self.context.get('request', False):
            if self.Meta.removed_fields_query in self.context['request'].query_params:
                field = self.context['request'].query_params[self.Meta.removed_fields_query].split(",")
                for f in field:
                    fields.pop(f)
        return fields


def make_serializer_class(model_, *fields_):
    if not fields_:
        fields_ = "__all__"
    else:
        fields_ = ["id", *fields_]

    class _Serializer(ModelSerializer):
        class Meta:
            model = model_
            fields = fields_

    _Serializer.__name__ = f"{model_.__name__}Serializer"
    return _Serializer


def make_info_serializer(model_, source, *fields_, many=False):
    class _Serializer(ModelSerializer):
        class Meta:
            model = model_
            fields = ["id", *fields_]

    _Serializer.__name__ = f"{model_.__name__}InfoSerializer"
    return _Serializer(read_only=True, source=source, many=many)
