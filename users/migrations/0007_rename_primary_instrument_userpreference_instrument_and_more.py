# Generated by Django 5.1.4 on 2025-02-06 03:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_instrument_userpreference_primary_instrument_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpreference',
            old_name='primary_instrument',
            new_name='instrument',
        ),
        migrations.RemoveField(
            model_name='userpreference',
            name='secondary_instrument',
        ),
    ]
