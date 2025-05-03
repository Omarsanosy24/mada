import os
import random
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
# from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class BasePagination(PageNumberPagination):
    page_size_query_param = "page_limit"
    max_page_size = 100


class ModelViewSet(ModelViewSet):
    pagination_class = BasePagination
    serializer_class: None

    # renderer_classes = (CustomJsonRender,)

    def paginate_queryset(self, queryset):
        if not getattr(queryset, "ordered", False):
            queryset = queryset.order_by("-id")
        if "nopagination" in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    def list(self, request, status=True, message=None):
        if "nopagination" in self.request.query_params:
            try:
                data = {
                    "results": super().list(request).data
                }
            except:
                data = {
                    "results": None
                }
        else:
            data = super().list(request).data
        data['status'] = status
        data['message'] = message
        return Response(data)

    def destroy(self, request, pk=None):
        super().destroy(request, pk)
        return self.list(request)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "status": True,
                "message": _("all is done"),
                "results": serializer.data
            }
        )

    def create(self, request):
        serializers = self.get_serializer(data=request.data)
        if serializers.is_valid():
            self.perform_create(serializers)
            return self.list(request)
        else:
            # return Response(
            #     {
            #         "status":False,
            #         "message":ser.errors
            #     }
            # )
            raise ValidationError(serializers.errors)

    def perform_create(self, serializers):
        serializers.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return self.list(request)
        else:
            return Response(
                {
                    "status": False,
                    "message": serializer.errors
                }
            )

    def perform_update(self, serializer):
        serializer.save()


class ModelViewSetIndividual(ModelViewSet):
    """
    in this we send create and update like the main ModelViewSet
    """

    def create(self, request):
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            self.perform_create(ser)
            return Response({
                "status": True,
                "message": _('done successfully'),
                "results": ser.data
            }, status=status.HTTP_201_CREATED)
        else:
            # return Response(
            #     {
            #         "status":False,
            #         "message":ser.errors
            #     }
            # )
            raise ValidationError(ser.errors)

    def perform_create(self, ser):
        ser.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(
                {
                    "status": True,
                    "message": None,
                    "results": serializer.data
                })
        else:
            return Response(
                {
                    "status": False,
                    "message": serializer.errors
                }
            )

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, pk=None):
        super().destroy(request, pk)
        return Response({
            "status": True,
            "message": _("deleted successfully")
        })

class ModelViewSetWithCaching(ModelViewSetIndividual):
    default_cache_time = 60 * 10

    @method_decorator(cache_page(default_cache_time))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    #

    def perform_create(self, ser):
        from django.core.cache import cache
        cache.clear()
        return super().perform_create(ser)

    def perform_update(self, ser):
        from django.core.cache import cache
        cache.clear()
        return super().perform_update(ser)

    def perform_destroy(self, instance):
        from django.core.cache import cache
        cache.clear()
        return super().perform_destroy(instance)
