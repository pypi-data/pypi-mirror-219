# Generated by Django 3.1.7 on 2021-08-19 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djautotask', '0096_merge_20210728_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountphysicallocation',
            name='primary',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='account_physical_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.accountphysicallocation'),
        ),
    ]
