# Generated by Django 3.2.6 on 2021-08-21 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dishmodel',
            name='dish_description',
            field=models.TextField(blank=True),
        ),
    ]