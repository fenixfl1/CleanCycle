# Generated by Django 4.2.6 on 2024-02-14 00:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0011_remove_savedposts_reazon_bloquedauthor_reason'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangesItems',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, max_length=1)),
                ('exchange_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('item_state', models.IntegerField(choices=[(1, 'Nuevo'), (2, 'Usado, Como nuevo'), (3, 'Usado')], default=3)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'verbose_name': 'Exchange Item',
                'verbose_name_plural': 'Exchange Items',
                'db_table': 'exchanges_items',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, max_length=1)),
                ('tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField()),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'db_table': 'tags',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Reactions',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, max_length=1)),
                ('reaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('reaction', models.IntegerField(choices=[(1, 'Like'), (2, 'Dislike')])),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, to_field='username')),
                ('exchange_item', models.ForeignKey(db_column='exchange_item', on_delete=django.db.models.deletion.CASCADE, related_name='exchange_item_reaction', to='exchanges.exchangesitems')),
            ],
            options={
                'verbose_name': 'Reaction',
                'verbose_name_plural': 'Reactions',
                'db_table': 'reactions',
            },
        ),
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
        migrations.CreateModel(
            name='ExhangeProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, max_length=1)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, to_field='username')),
                ('desired_item', models.ForeignKey(db_column='desired_item', on_delete=django.db.models.deletion.CASCADE, related_name='desired_item', to='exchanges.exchangesitems')),
                ('item_offered', models.ForeignKey(db_column='item_offered', on_delete=django.db.models.deletion.CASCADE, related_name='item_offered', to='exchanges.exchangesitems')),
            ],
            options={
                'verbose_name': 'Exchange proposal',
                'db_table': 'exchage_proposal',
            },
        ),
        migrations.AddField(
            model_name='exchangesitems',
            name='tags',
            field=models.ManyToManyField(db_column='tags', to='exchanges.tags'),
        ),
        migrations.AddConstraint(
            model_name='exhangeproposal',
            constraint=models.UniqueConstraint(fields=('item_offered', 'desired_item'), name='pk_exchage_proposal'),
        ),
    ]
