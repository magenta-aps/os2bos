# Generated by Django 2.2.26 on 2022-01-18 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0102_auto_20220110_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='dst_handicap',
            field=models.BooleanField(blank=True, default=True, help_text="Hvorvidt denne paragraf skal bruges til DST udtræk for 'Handicapkompenserende indsatser'.", verbose_name="DST 'Handicapkompenserende indsatser'"),
        ),
    ]