# Generated by Django 5.1 on 2024-08-15 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amenity',
            options={'verbose_name_plural': 'Amenities'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name_plural': 'Images'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name_plural': 'Locations'},
        ),
        migrations.AlterModelOptions(
            name='propertyinfo',
            options={'verbose_name_plural': 'Property Info'},
        ),
    ]
