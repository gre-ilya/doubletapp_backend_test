from django.contrib import admin

from app.internal.admin.admin_user import AdminUserAdmin
from app.internal import models

admin.site.site_title = "Backend course"
admin.site.site_header = "Backend course"

"""Adding ORM objects to django admin panel"""
admin.site.register(models.service_user.ServiceUser)
admin.site.register(models.bank_account.BankAccount)
admin.site.register(models.card.Card)
