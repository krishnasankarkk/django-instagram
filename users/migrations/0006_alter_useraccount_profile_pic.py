# Generated by Django 4.2.7 on 2024-01-09 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_useraccount_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='profile_pic',
            field=models.URLField(blank=True),
        ),
    ]
