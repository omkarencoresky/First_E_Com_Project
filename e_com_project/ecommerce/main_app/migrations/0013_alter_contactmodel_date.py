# Generated by Django 4.2.11 on 2024-05-22 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_contactmodel_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmodel',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
