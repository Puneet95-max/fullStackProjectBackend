# Generated by Django 3.2.12 on 2024-06-12 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_alter_dailyreport_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreport',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
