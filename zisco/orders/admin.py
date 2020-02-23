from django.contrib import admin

from .models import (
    Quotation, QuotationItem
)


class QItemInline(admin.TabularInline):
    model = QuotationItem
    fields = ("product", "qty")


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    inlines = (QItemInline,)
    list_display = ("number", "customer", "created", "expires", "total")
    list_filter = ("created", "expires")
