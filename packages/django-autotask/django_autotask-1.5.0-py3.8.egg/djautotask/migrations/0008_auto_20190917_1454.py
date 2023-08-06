# Generated by Django 2.1.11 on 2019-09-17 14:54

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djautotask', '0007_auto_20190917_1009'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('last_activity_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='queue',
            options={},
        ),
        migrations.AlterModelOptions(
            name='ticketpriority',
            options={'verbose_name_plural': 'Ticket priorities'},
        ),
        migrations.AlterModelOptions(
            name='ticketstatus',
            options={'verbose_name_plural': 'Ticket statuses'},
        ),
        migrations.AddField(
            model_name='ticket',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Account'),
        ),
    ]
