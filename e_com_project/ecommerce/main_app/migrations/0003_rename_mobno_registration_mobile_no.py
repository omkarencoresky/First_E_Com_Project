# Generated by Django 4.2.11 on 2024-05-16 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_remove_registration_last_login'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='mobno',
            new_name='mobile_no',
        ),
    ]
