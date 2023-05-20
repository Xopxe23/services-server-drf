from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client


class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}: {self.full_price}'


class Plan(models.Model):
    PLAN_TYPES = (
        ("full", "Full"),
        ("student", "Student"),
        ("discount", "Discount")
    )
    plan_type = models.CharField(choices=PLAN_TYPES)
    discount_percents = models.PositiveIntegerField(default=0,
                                                    validators=[MaxValueValidator(100)])

    def __str__(self):
        return f'{self.plan_type}: -{self.discount_percents}%'


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.client} - {self.service}'
