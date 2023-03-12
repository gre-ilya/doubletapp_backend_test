# Generated by Django 4.2a1 on 2023-02-28 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("app", "0004_alter_serviceuser_is_premium")]

    operations = [
        migrations.CreateModel(
            name="BankAccount",
            fields=[
                ("id", models.CharField(max_length=20, primary_key=True, serialize=False)),
                ("rcbic", models.CharField(max_length=9)),
                ("corr_account", models.CharField(max_length=20)),
                ("inn", models.CharField(max_length=10)),
                ("kpp", models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name="Card",
            fields=[
                ("id", models.CharField(max_length=16, primary_key=True, serialize=False)),
                ("expire_month", models.IntegerField()),
                ("expire_year", models.IntegerField()),
                ("owner_name", models.CharField(max_length=128, null=True)),
                ("cvv", models.CharField(max_length=3)),
                (
                    "account_number",
                    models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to="app.bankaccount"),
                ),
            ],
        ),
    ]
