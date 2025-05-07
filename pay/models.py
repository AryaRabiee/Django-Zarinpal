# payment/models.py
from django.db import models
from enum import Enum

class PaymentStatusType(Enum):
    success = "success"
    failed = "failed"

class Payment(models.Model):
    amount = models.IntegerField()
    authority_id = models.CharField(max_length=100)
    ref_id = models.CharField(max_length=100, null=True, blank=True)
    response_code = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[(t.value, t.name) for t in PaymentStatusType])
    response_json = models.JSONField(null=True, blank=True)

class OrderStatusType(Enum):
    success = "success"
    canceled = "canceled"

class Order(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[(t.value, t.name) for t in OrderStatusType])
