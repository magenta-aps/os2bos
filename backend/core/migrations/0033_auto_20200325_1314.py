# Generated by Django 2.2.9 on 2020-03-25 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_remove_activity_payment_plan_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentschedule',
            name='activity',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_plan', to='core.Activity', verbose_name='aktivitet'),
        ),
    ]
