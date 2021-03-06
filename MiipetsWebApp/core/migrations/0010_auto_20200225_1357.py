# Generated by Django 3.0.3 on 2020-02-25 13:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200225_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicebooking',
            name='price',
            field=models.PositiveIntegerField(default=25, validators=[django.core.validators.MinValueValidator(25)]),
        ),
        migrations.AlterField(
            model_name='servicebooking',
            name='price_in_cents',
            field=models.PositiveIntegerField(default=2500, validators=[django.core.validators.MinValueValidator(2500)]),
        ),
        migrations.AlterField(
            model_name='sitterservices',
            name='price',
            field=models.PositiveIntegerField(default=25, validators=[django.core.validators.MinValueValidator(25)]),
        ),
    ]
