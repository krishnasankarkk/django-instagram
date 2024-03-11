# Generated by Django 4.2.7 on 2024-02-06 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_useraccount_profile_pic'),
        ('notifications', '0002_alter_notification_sender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='sender',
        ),
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ManyToManyField(to='users.useraccount'),
        ),
    ]