import uuid

from django.db import models


class StripeConfig(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100, unique=True)
    public_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    restricted_key = models.CharField(max_length=255, null=True, blank=True)
    webhook_secret = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Stripe config"
        verbose_name_plural = "Stripe configs"

    def __str__(self):
        return f"<StripeConfig: {self.name}>"
