# Generated by Django 3.2.10 on 2022-02-20 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_recipeingredient_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredient',
            name='quantity_as_float',
            field=models.FloatField(blank=True, null=True),
        ),
    ]