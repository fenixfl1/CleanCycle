# Generated by Django 4.2.6 on 2024-02-08 14:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0006_posts_preview_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, max_length=1)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, to_field='username')),
                ('post_id', models.ForeignKey(db_column='post_id', on_delete=django.db.models.deletion.CASCADE, related_name='saved_posts', to='posts.posts')),
                ('username', models.ForeignKey(db_column='username', on_delete=django.db.models.deletion.CASCADE, related_name='user_saved_posts', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'verbose_name': 'Saved Post',
                'verbose_name_plural': 'Saved Posts',
                'db_table': 'saved_posts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='savedposts',
            constraint=models.UniqueConstraint(fields=('post_id', 'username'), name='unique_saved_post_user'),
        ),
    ]
