# Generated by Django 4.0.4 on 2022-05-12 16:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_added_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='added_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 5, 12, 16, 30, 4, 325516)),
            preserve_default=False,
        ),
    ]
