# Generated by Django 5.0 on 2024-08-01 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quotes', '0003_rename__from_notification_from_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='post_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
