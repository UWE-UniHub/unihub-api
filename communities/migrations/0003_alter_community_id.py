# Generated by Django 5.0.1 on 2025-03-04 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
