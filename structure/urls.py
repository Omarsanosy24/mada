from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StaticDataViewSet, BannersView, BlogsView, ProductView, H_Vac_CategoryViewSet, OurClientsView, \
    CapacityView, ProductGeneratorSetViewSet, CategoryGeneratorViewSet, FireProductsViewSet

router = DefaultRouter()
router.register("static-data", StaticDataViewSet)
router.register("banners", BannersView)
router.register("blogs", BlogsView)
router.register("product", ProductView)
router.register("h-vac", H_Vac_CategoryViewSet)
router.register("our-clients", OurClientsView)
router.register("capacity", CapacityView)
router.register("product-generator-set", ProductGeneratorSetViewSet)
router.register("category-generator-set", CategoryGeneratorViewSet)
router.register("fire-products", FireProductsViewSet)


app_name = "static_data"
urlpatterns = [
    path('', include(router.urls)),
]
