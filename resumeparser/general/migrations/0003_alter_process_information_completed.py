# Generated by Django 4.2.13 on 2024-07-08 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_process_information_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process_information',
            name='completed',
            field=models.BooleanField(default=True),
        ),
    ]
