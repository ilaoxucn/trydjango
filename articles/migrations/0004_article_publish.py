# Generated by Django 3.2.10 on 2022-01-30 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20220130_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publish',
            field=models.DateField(blank=True, null=True),
        ),
    ]