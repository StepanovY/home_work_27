# Generated by Django 4.1.2 on 2022-10-23 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ad',
            old_name='images',
            new_name='image',
        ),
    ]
