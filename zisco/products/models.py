from functools import reduce

from django.db import models
from django.contrib.humanize.templatetags.humanize import intcomma as ic

from zisco.core.models import UUIDModel


class Category(UUIDModel):
    name = models.CharField(
        max_length=255,
    )

    class Meta:
        verbose_name_plural = "product categories"

    def __str__(self):
        return self.name


class Product(UUIDModel):
    category = models.ForeignKey(
        to="products.Category",
        on_delete=models.CASCADE,
        related_name="products",
    )
    measurement = models.CharField(
        null=True, blank=True,
        help_text="e.g Tonnes:Tonne:T",
        max_length=255
    )
    code = models.CharField(max_length=255, null=True, blank=True, )
    name = models.CharField(
        max_length=255,
    )
    _price = models.DecimalField(
        max_digits=19, decimal_places=2, default=2
    )

    class Meta:
        verbose_name_plural = "products"

    def __str__(self):
        return self.name

    @property
    def stock(self):
        return sum([i.units for i in self.inventory.iterator()])

    @property
    def stock_alt(self):
        if self.measurement and len(self.measurement.split(":")) == 3:
            plu, sin, si = tuple(self.measurement.split(":"))
            return f"{ic(self.stock)} {plu.title()}"
        return f"{ic(self.stock)}"

    @property
    def measles(self):
        if self.measurement and len(self.measurement.split(":")) == 3:
            return self.measurement.split(":")[0]
        return "Units"

    @property
    def in_stock(self):
        return self.stock > 1

    @property
    def price(self):
        return f"Z ${ic(self._price)}"

    @property
    def price_alt(self):
        if self.measurement:
            if len(self.measurement.split(":")) == 3:
                plu, sin, si = tuple(self.measurement.split(":"))
                return f"Z ${ic(self._price)} per {sin.title()}"
        return f"Z ${ic(self._price)}"

    @price.setter
    def price(self, value):
        self._price = value


class Inventory(UUIDModel):
    product = models.ForeignKey(
        to="products.Product",
        on_delete=models.CASCADE,
        related_name="inventory"
    )
    man = models.DateField()
    units = models.IntegerField()

    class Meta:
        verbose_name_plural = "products inventory"

    def __str__(self):
        return f"{self.man} - {self.units_alt} of {self.product}"

    @property
    def units_alt(self):
        if self.product.measurement:
            ms = self.product.measurement
            if len(ms.split(":")) == 3:
                plu, sin, si = tuple(ms.split(":"))
                return f"{ic(self.units)} {plu.title()}"
        return self.units
