

import stripe
from stripe.error import AuthenticationError
from django.conf import settings

from .helpers import color as c
from .models import StripeConfig


SILLY_STRIPE = {
    'is_configured': False,
    'STRIPE_PUBLIC_KEY': None,
    'STRIPE_SECRET_KEY': None,
    'STRIPE_WEBHOOK_SECRET': None,
}

for key in settings.SILLY_STRIPE:
    SILLY_STRIPE[key] = settings.SILLY_STRIPE[key]


if SILLY_STRIPE['config_name'] is not None and \
        StripeConfig.objects.filter(name=SILLY_STRIPE['config_name']).exists():
    stripe_config = StripeConfig.objects.get(name=SILLY_STRIPE['config_name'])
    stripe.api_key = stripe_config.secret_key
    SILLY_STRIPE['is_configured'] = True

    print('=== Customers: ', stripe.Customer.list())
    print('=== Products: ', stripe.Product.list())

else:
    print(f"{c['warning']}DJANGO-SILLY-STRIPE IS NOT CONFIGURED{c['end']}")
