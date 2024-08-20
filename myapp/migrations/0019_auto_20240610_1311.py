# Generated by Django 3.2.12 on 2024-06-10 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_alter_teamlead_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='project',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='myapp.project'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='manager',
            name='project',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='managers', to='myapp.project'),
            preserve_default=False,
        ),
    ]
