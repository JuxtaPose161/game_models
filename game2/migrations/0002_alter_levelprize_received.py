# Generated by Django 5.1.1 on 2024-10-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='levelprize',
            name='received',
            field=models.DateField(blank=True, null=True),
        ),
    ]
