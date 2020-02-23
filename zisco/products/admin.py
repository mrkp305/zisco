from django.contrib import admin

from .models import (
    Category, Product, Inventory
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created",)
    list_filter = ("created",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "price_alt", "category", "created", "modified",)
    list_filter = ("category",)
    search_fields = ("name",)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("id", "man", "units_alt", )
