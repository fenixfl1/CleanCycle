# Generated by Django 4.2.6 on 2024-02-25 01:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0011_remove_savedposts_reazon_bloquedauthor_reason'),
        ('exchanges', '0002_reactions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagesXExchangesItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, max_length=1)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, to_field='username')),
                ('exchange_item_id', models.ForeignKey(db_column='exchange_item_id', on_delete=django.db.models.deletion.CASCADE, related_name='exchange_items_image', to='exchanges.exchangesitems')),
                ('image_id', models.ForeignKey(db_column='image_id', on_delete=django.db.models.deletion.CASCADE, related_name='exchange_items_image', to='posts.images')),
            ],
            options={
                'verbose_name': 'Image for exchange item',
                'verbose_name_plural': 'Images for exchange items',
                'db_table': 'images_x_exchange_items',
                'ordering': ['image_id'],
            },
        ),
    ]
