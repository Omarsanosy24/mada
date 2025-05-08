from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StaticDataViewSet, BannersView, BlogsView

router = DefaultRouter()
router.register("static-data", StaticDataViewSet)
router.register("banners", BannersView)
router.register("blogs", BlogsView)

app_name = "static_data"
urlpatterns = [
    path('', include(router.urls)),
]
