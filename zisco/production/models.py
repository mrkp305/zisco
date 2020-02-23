from django.db import models

from zisco.core.models import UUIDModel


class DispatchPlan(UUIDModel):
    order = models.ForeignKey(
        to="orders.Order",
        on_delete=models.CASCADE,
        related_name="dispatch_plan"
    )

    class Meta:
        verbose_name_plural = "dispatch plans"

    def __str__(self):
        return self.order
