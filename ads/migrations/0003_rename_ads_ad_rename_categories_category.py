# Generated by Django 4.1.2 on 2022-10-16 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_ads_is_published_alter_ads_price_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ads',
            new_name='Ad',
        ),
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
    ]