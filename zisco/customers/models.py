from django.db import models
from django.contrib.humanize.templatetags.humanize import intcomma as ic

from zisco.core.models import UUIDModel


class Req(UUIDModel):
    customer = models.ForeignKey(
        to="users.Customer",
        on_delete=models.CASCADE,
        related_name="requests"
    )

    class Meta:
        verbose_name = "product request"
        verbose_name_plural = "product requests"

    def __str__(self):
        return ""


class ReqItem(UUIDModel):
    request = models.ForeignKey(
        to="Req",
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        to="products.Product",
        on_delete=models.CASCADE,
        related_name="requested"
    )
    qty = models.IntegerField()

    class Meta:
        verbose_name = "request item"
        verbose_name_plural = "request items"

    def __str__(self):
        return f"{self.alt_units} of {self.product.name}"

    @property
    def alt_units(self):
        if self.product.measurement and len(self.product.measurement.split(":")) == 3:
            _p, _sl, _ss = self.product.measurement.split(":")
            return f"{ic(self.qty)} {_p}"
        return f"{ic(self.qty)} units"
