# Generated by Django 4.2.6 on 2023-10-26 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_postimages_options_alter_postimages_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='front_page',
            field=models.TextField(default=''),
        ),
    ]
