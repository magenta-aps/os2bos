# Generated by Django 2.2.9 on 2020-06-02 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_auto_20200528_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='created_new',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='oprettet'),
        ),
        migrations.AddField(
            model_name='activity',
            name='modified_new',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='modificeret'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user_created_new',
            field=models.CharField(blank=True, max_length=128, verbose_name='bruger der har oprettet'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user_modified_new',
            field=models.CharField(blank=True, max_length=128, verbose_name='bruger der har modificeret'),
        ),
        migrations.AddField(
            model_name='appropriation',
            name='created_new',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='oprettet'),
        ),
        migrations.AddField(
            model_name='appropriation',
            name='modified_new',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='modificeret'),
        ),
        migrations.AddField(
            model_name='appropriation',
            name='user_created_new',
            field=models.CharField(blank=True, max_length=128, verbose_name='bruger der har oprettet'),
        ),
        migrations.AddField(
            model_name='appropriation',
            name='user_modified_new',
            field=models.CharField(blank=True, max_length=128, verbose_name='bruger der har modificeret'),
        ),
        migrations.AddField(
            model_name='case',
            name='created_new',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='oprettet'),
        ),
        migrations.AddField(
            model_name='case',
            name='modified_new',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='modificeret'),
        ),
        migrations.AddField(
            model_name='case',
            name='user_created_new',
            field=models.CharField(blank=True, max_length=128, verbose_name='bruger der har oprettet'),
        ),
        migrations.AddField(
            model_name='case',
            name='user_modified_new',
            field=models.CharField(blank=True, max_length=128, verbose_name='bruger der har modificeret'),
        ),
        migrations.AddField(
            model_name='historicalcase',
            name='created_new',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='oprettet'),
        ),
        migrations.AddField(
            model_name='historicalcase',
            name='modified_new',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='modificeret'),
        ),
        migrations.AddField(
            model_name='historicalcase',
            name='user_created_new',
            field=models.CharField(blank=True, max_length=128, verbose_name='bruger der har oprettet'),
        ),
        migrations.AddField(
            model_name='historicalcase',
            name='user_modified_new',
            field=models.CharField(blank=True, max_length=128, verbose_name='bruger der har modificeret'),
        ),
        migrations.AddField(
            model_name='relatedperson',
            name='created_new',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='oprettet'),
        ),
        migrations.AddField(
            model_name='relatedperson',
            name='modified_new',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='modificeret'),
        ),
        migrations.AddField(
            model_name='relatedperson',
            name='user_created_new',
            field=models.CharField(blank=True, max_length=128, verbose_name='bruger der har oprettet'),
        ),
        migrations.AddField(
            model_name='relatedperson',
            name='user_modified_new',
            field=models.CharField(blank=True, max_length=128, verbose_name='bruger der har modificeret'),
        ),
    ]
