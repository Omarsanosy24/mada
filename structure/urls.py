from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StaticDataViewSet


router = DefaultRouter()
router.register("static-data", StaticDataViewSet, basename="static-data")

app_name = "static_data"
urlpatterns = [
    path('', include(router.urls)),
]
