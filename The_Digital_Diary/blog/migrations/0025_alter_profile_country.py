# Generated by Django 5.0.7 on 2024-08-19 00:02

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_alter_profile_state_city_alter_profile_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
    ]
