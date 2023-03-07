from django.db import models


class BankAccount(models.Model):
    """Model for Russian Bank account:
    id - account number
    rcbic - Russian Central Bank Identification Code (BIC)
    corr_account - correspondent account
    inn - Taxpayer Identification Number (INN)
    kpp - Tax Registration Reason Code (KPP)
    """

    id = models.CharField(primary_key=True, max_length=20, auto_created=False)
    rcbic = models.CharField(max_length=9)
    corr_account = models.CharField(max_length=20)
    inn = models.CharField(max_length=10)
    kpp = models.CharField(max_length=9)
    balance = models.DecimalField(max_digits=32, decimal_places=2, default=0)
