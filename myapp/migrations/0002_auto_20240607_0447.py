# Generated by Django 3.2.12 on 2024-06-07 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roles',
            name='id',
        ),
        migrations.AlterField(
            model_name='roles',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
