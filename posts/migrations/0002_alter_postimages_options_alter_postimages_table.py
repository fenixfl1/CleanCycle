# Generated by Django 4.2.6 on 2023-10-22 17:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="postimages",
            options={
                "ordering": ["image_id"],
                "verbose_name": "Post Image",
                "verbose_name_plural": "Posts Images",
            },
        ),
        migrations.AlterModelTable(
            name="postimages",
            table="post_images",
        ),
    ]
