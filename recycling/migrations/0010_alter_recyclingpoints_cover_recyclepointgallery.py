# Generated by Django 4.2.6 on 2023-11-28 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_alter_posts_options'),
        ('recycling', '0009_recyclingpoints_email_recyclingpoints_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recyclingpoints',
            name='cover',
            field=models.TextField(blank=True, default='https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found.jpg', null=True),
        ),
        migrations.CreateModel(
            name='RecyclePointGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('state', models.BooleanField(default=True, max_length=1)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, to_field='username')),
                ('image', models.ForeignKey(db_column='image_id', on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_image', to='posts.images')),
                ('recycling_point', models.ForeignKey(db_column='recycle_point_id', on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_recycling_point', to='recycling.recyclingpoints')),
            ],
            options={
                'db_table': 'recycle_point_gallery',
            },
        ),
    ]
