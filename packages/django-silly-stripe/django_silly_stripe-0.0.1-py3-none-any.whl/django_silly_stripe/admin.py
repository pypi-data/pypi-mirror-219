from django.contrib import admin
from .models import StripeConfig


class StripeConfigAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


admin.site.register(StripeConfig, StripeConfigAdmin)
