# Generated by Django 3.1 on 2020-09-17 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20200917_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='seed',
            field=models.CharField(max_length=100),
        ),
    ]