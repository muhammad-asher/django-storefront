from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.models import Product
from store.admin import ProductAdmin
from tags.models import TagItem


# Register your models here.
class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    min_num = 1
    extra = 0
    model = TagItem


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)