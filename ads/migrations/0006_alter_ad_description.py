# Generated by Django 4.1.2 on 2022-11-15 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0005_alter_ad_name_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]