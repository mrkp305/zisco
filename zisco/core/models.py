import uuid

from django.db import models

from model_utils.models import TimeStampedModel


class UUIDModel(TimeStampedModel):
    uuid_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    class Meta:
        abstract = True
