from django.db import models


class ServiceUser(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=False)
    username = models.CharField(null=True, max_length=32)
    first_name = models.CharField(null=True, max_length=64)
    last_name = models.CharField(null=True, max_length=64)
    language_code = models.CharField(null=True, max_length=3)
    phone_number = models.CharField(null=True, max_length=15)

    def __str__(self):
        return self.username
