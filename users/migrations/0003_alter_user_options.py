# Generated by Django 4.2.6 on 2023-10-20 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username'], 'verbose_name': 'User'},
        ),
    ]
