# Generated by Django 4.2.5 on 2023-09-23 14:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("usersApp", "0004_alter_onetimetoken_expiration_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onetimetoken",
            name="expiration_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 23, 14, 28, 41, 353399, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]