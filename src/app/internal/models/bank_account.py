from app.internal.models.service_user import ServiceUser
from django.db import models


class BankAccount(models.Model):
    id = models.CharField(primary_key=True, max_length=20, auto_created=False)
    user = models.ForeignKey(ServiceUser, on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=32, decimal_places=2, default=0)
