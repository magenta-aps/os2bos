# Generated by Django 2.2.1 on 2019-10-21 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("core", "0004_auto_20191016_1459")]

    operations = [
        migrations.RemoveField(model_name="paymentschedule", name="payment_id")
    ]
