# Generated by Django 5.1 on 2024-08-20 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0012_alter_location_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='updated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='updated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='updated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='propertyinfo',
            name='updated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
