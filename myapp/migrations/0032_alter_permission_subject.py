# Generated by Django 3.2.12 on 2024-06-13 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0031_auto_20240613_0804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='subject',
            field=models.CharField(max_length=50),
        ),
    ]
