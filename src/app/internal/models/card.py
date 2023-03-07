from django.db import models
from app.internal.models.bank_account import BankAccount


class Card(models.Model):
    id = models.CharField(primary_key=True, auto_created=False, max_length=16)
    account_number = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING)
    expire_month = models.IntegerField()
    expire_year = models.IntegerField()
    owner_name = models.CharField(max_length=128, null=True)
    cvv = models.CharField(max_length=3)
    balance = models.DecimalField(max_digits=32, decimal_places=2, default=0)