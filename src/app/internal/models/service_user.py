from django.db import models


class ServiceUser(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=False)
    is_bot = models.BooleanField()
    username = models.CharField(null=True, max_length=32)
    first_name = models.CharField(null=True, max_length=64)
    last_name = models.CharField(null=True, max_length=64)
    language_code = models.CharField(null=True, max_length=3)
    phone_number = models.CharField(null=True, max_length=15)

    def __iter__(self):
        """Return field names as str"""
        for field_name in self._meta.get_fields():
            yield str(field_name).split(".")[-1]

    def __str__(self):
        return self.username
