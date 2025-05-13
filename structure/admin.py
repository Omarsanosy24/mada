from django.contrib import admin
from .models import StaticData, ServicesModel, ProductModel, CapacityModel, BrandsModel, BlogsModel, BannersModel, \
    OurClientsModel, H_Vac_CategoryModel, ProductGeneratorSet, CategoryGeneratorSet, ContactKindModel


# Register your models here.


@admin.register(StaticData)
class StaticDataAdmin(admin.ModelAdmin):
    pass


@admin.register(ServicesModel)
class ServicesModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    pass


@admin.register(CapacityModel)
class CapacityModelAdmin(admin.ModelAdmin):
    pass


@admin.register(BrandsModel)
class BrandsModelAdmin(admin.ModelAdmin):
    pass


@admin.register(BlogsModel)
class BlogsModelAdmin(admin.ModelAdmin):
    pass


@admin.register(BannersModel)
class BannersModelAdmin(admin.ModelAdmin):
    pass


@admin.register(OurClientsModel)
class OurClientsModelAdmin(admin.ModelAdmin):
    pass


@admin.register(H_Vac_CategoryModel)
class H_Vac_CategoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductGeneratorSet)
class ProductGeneratorSetAdmin(admin.ModelAdmin):
    pass


@admin.register(CategoryGeneratorSet)
class CategoryGeneratorSetAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactKindModel)
class ContactKindModelAdmin(admin.ModelAdmin):
    pass
