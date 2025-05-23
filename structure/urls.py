from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StaticDataViewSet, BannersView, BlogsView, ProductView, H_Vac_CategoryViewSet, OurClientsView, \
    CapacityView, ProductGeneratorSetViewSet, CategoryGeneratorViewSet, FireProductsViewSet, BrandsViewSet, \
    BrandGeneratorSetViewSet, ContactUsModelViewSet, ContactKindModelViewSet, ClientKindModelViewSet, \
    NumOfPageForAllProductsView

router = DefaultRouter()
router.register("static-data", StaticDataViewSet)
router.register("banners", BannersView)
router.register("blogs", BlogsView)
router.register("product", ProductView)
router.register("h-vac", H_Vac_CategoryViewSet)
router.register("our-clients", OurClientsView)
router.register("kind-clients", ClientKindModelViewSet)
router.register("capacity", CapacityView)
router.register("product-generator-set", ProductGeneratorSetViewSet)
router.register("category-generator-set", CategoryGeneratorViewSet)
router.register("fire-products", FireProductsViewSet)
router.register("brands", BrandsViewSet)
router.register("brand-generator-set", BrandGeneratorSetViewSet)
router.register("contact-us", ContactUsModelViewSet)
router.register("contact-kind", ContactKindModelViewSet)


app_name = "static_data"
urlpatterns = [
    path('', include(router.urls)),
    path('num-of-page/', NumOfPageForAllProductsView.as_view(), name="num-of-page"),
]
