from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_dailyreport_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyreport',
            name='created_at',
            field=models.DateField(auto_now_add=True, default='2024-06-12'),  # Replace '2024-06-12' with a valid date
            preserve_default=False,
        ),
    ]
