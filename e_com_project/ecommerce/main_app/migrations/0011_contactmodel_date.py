# Generated by Django 4.2.11 on 2024-05-22 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_alter_billing_details_for_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmodel',
            name='date',
            field=models.DateTimeField(default=None),
        ),
    ]
