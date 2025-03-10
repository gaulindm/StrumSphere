# Generated by Django 5.1.4 on 2025-01-25 11:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userpreference_delete_userpreferences'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreference',
            name='is_printing_alternate_chord',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userpreference', to=settings.AUTH_USER_MODEL),
        ),
    ]
