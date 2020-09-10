# Generated by Django 2.2.13 on 2020-07-22 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0080_auto_20200721_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentschedule',
            name='payment_cost_type',
            field=models.CharField(blank=True, choices=[('FIXED', 'fast beløb'), ('PER_UNIT', 'pris pr. enhed'), ('GLOBAL_RATE', 'takst')], default='FIXED', max_length=128, null=True, verbose_name='betalingspristype'),
        ),
        migrations.AlterField(
            model_name='paymentschedule',
            name='payment_type',
            field=models.CharField(choices=[('ONE_TIME_PAYMENT', 'Engangsudgift'), ('RUNNING_PAYMENT', 'Fast beløb, løbende'), ('PER_HOUR_PAYMENT', 'Takst pr. time'), ('PER_DAY_PAYMENT', 'Takst pr. døgn'), ('PER_KM_PAYMENT', 'Takst pr. kilometer'), ('INDIVIDUAL_PAYMENT', 'Individuel')], max_length=128, verbose_name='betalingstype'),
        ),
    ]