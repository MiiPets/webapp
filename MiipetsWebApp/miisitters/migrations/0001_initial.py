# Generated by Django 3.0.1 on 2020-01-02 11:45

import core.models
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MiiSitter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('contact_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('profile_picture', models.ImageField(upload_to=core.models.image_directory_path)),
                ('bio', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SitterServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('WALK', 'Walker'), ('BOARD', 'Boarding'), ('SIT', 'House Sitting'), ('DAYCARE', 'Daycare'), ('FEED', 'Feeder')], default='DAYCARE', max_length=50)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('score', models.FloatField()),
                ('sitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miisitters.MiiSitter')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
