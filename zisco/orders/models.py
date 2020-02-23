from django.db import models
from django.contrib.humanize.templatetags.humanize import intcomma as ic
from django.utils import timezone

from model_utils.models import StatusModel
from model_utils.choices import Choices

from zisco.core.models import UUIDModel


class Order(UUIDModel, StatusModel):
    STATUS = Choices("new", "completed", "cancelled", )

    customer = models.ForeignKey(
        to="users.Customer",
        on_delete=models.CASCADE,
        related_name="orders",
    )

    class Meta:
        verbose_name_plural = "orders"

    def __str__(self):
        return f"Order #{self.number} - {self.customer}"

    @property
    def number(self):
        return str(self.id).zfill(4)

    def _total(self):
        return sum([i._line_total() for i in self.items.iterator()])

    @property
    def total(self):
        return f"Z ${ic(self._total())}"


class OrderItem(UUIDModel):
    order = models.ForeignKey(
        to="orders.Order",
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        to="products.Product",
        on_delete=models.CASCADE,
        related_name="order_appearance"
    )
    qty = models.IntegerField()
    _price = models.DecimalField(
        max_digits=19, decimal_places=2,
    )

    class Meta:
        verbose_name_plural = "order items"
        unique_together = ("product", "order")

    def __str__(self):
        return self.product

    def _line_total(self):
        return self.qty * self._price

    @property
    def line_total(self):
        return f"Z $ {self._line_total()}"

    @property
    def alt_qty(self):
        if self.product.measurement and len(self.product.measurement.split(":")) == 3:
            _p, _sl, _ss = self.product.measurement.split(":")
            return f"{ic(self.qty)} {_p}"
        return f"{ic(self.qty)} units"

    @property
    def price(self):
        return f"Z ${ic(self._price)}"

    @property
    def price_alt(self):
        pms = self.product.measurement
        if pms:
            if len(pms.split(":")) == 3:
                plu, sin, si = tuple(pms.split(":"))
                return f"Z ${ic(self._price)} per {sin.title()}"
        return f"Z ${ic(self._price)}"

    @price.setter
    def price(self, value):
        self._price = value


class Quotation(UUIDModel):
    customer = models.ForeignKey(
        to="users.Customer",
        on_delete=models.CASCADE,
        related_name="quotations",
    )
    expires = models.DateField()

    class Meta:
        verbose_name_plural = "quotations"

    @property
    def number(self):
        return self.id

    def __str__(self):
        return f"#{self.number} - {self.customer} [{self.expires}]"

    def _total(self):
        return sum([i._line_total() for i in self.items.iterator()])

    @property
    def total(self):
        return f"Z ${ic(self._total())}"

    @property
    def has_expired(self):
        return self.expires < timezone.now().date()


class QuotationItem(UUIDModel):
    quotation = models.ForeignKey(
        to="Quotation",
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        to="products.Product",
        on_delete=models.CASCADE,
    )
    qty = models.IntegerField(
        verbose_name="quantity",
    )
    _price = models.DecimalField(
        max_digits=19, decimal_places=2, editable=False
    )

    class Meta:
        verbose_name_plural = "quotation items"
        unique_together = ("quotation", "product")

    def __str__(self):
        pms = self.product.measurement
        if pms:
            if len(pms.split(":")) == 3:
                plu, sin, si = tuple(pms.split(":"))
                return f"{self.qty} {plu.title()} of {self.product}"

        return f"{self.qty} x {self.product}"

    @property
    def price(self):
        return f"Z ${ic(self._price)}"

    @property
    def price_alt(self):
        pms = self.product.measurement
        if pms:
            if len(pms.split(":")) == 3:
                plu, sin, si = tuple(pms.split(":"))
                return f"Z ${ic(self._price)} per {sin.title()}"
        return f"Z ${ic(self._price)}"

    @price.setter
    def price(self, value):
        self._price = value

    def _line_total(self):
        return self._price * self.qty

    @property
    def line_total(self):
        return f"Z ${ic(self._line_total())}"

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk:
            self.price = self.product._price
        super().save(*args, **kwargs)
