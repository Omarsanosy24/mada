from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StaticDataViewSet, BannersView, BlogsView, ProductView, H_Vac_CategoryViewSet, OurClientsView

router = DefaultRouter()
router.register("static-data", StaticDataViewSet)
router.register("banners", BannersView)
router.register("blogs", BlogsView)
router.register("product", ProductView)
router.register("h-vac", H_Vac_CategoryViewSet)
router.register("our-clients", OurClientsView)


app_name = "static_data"
urlpatterns = [
    path('', include(router.urls)),
]
