# Generated by Django 3.2.12 on 2024-06-12 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_alter_dailyreport_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailyreport',
            name='created_at',
        ),
    ]
