# Generated by Django 4.2.5 on 2023-09-23 03:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("usersApp", "0003_alter_onetimetoken_expiration_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimetoken",
            name="expiration_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 23, 3, 31, 7, 454405, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]