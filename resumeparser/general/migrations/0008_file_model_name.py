# Generated by Django 4.2.13 on 2024-07-24 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0007_remove_process_information_mymodel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='file_model',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
