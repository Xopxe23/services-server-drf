import time

from celery import shared_task
from celery_singleton import Singleton
from django.conf import settings
from django.core.cache import cache
from django.db.models import F


@shared_task(base=Singleton)
def set_price(subscription_id):
    from services.models import Subscription

    time.sleep(10)

    subscription = Subscription.objects.filter(id=subscription_id).annotate(
        annotated_price=F("service__full_price") - F("service__full_price") * F("plan__discount_percents") / 100.00
    ).first()
    subscription.price = subscription.annotated_price
    subscription.save()
    cache.delete(settings.PRICE_CACHE_NAME)
