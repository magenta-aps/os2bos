# Generated by Django 2.2.26 on 2022-02-17 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0107_remove_soft_deleted_activities'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='activity',
            name='unique_main_activity',
        ),
        migrations.AddConstraint(
            model_name='activity',
            constraint=models.UniqueConstraint(condition=models.Q(('activity_type', 'MAIN_ACTIVITY'), ('modifies__isnull', True)), fields=('appropriation',), name='unique_main_activity'),
        ),
    ]