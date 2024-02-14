from django.db import models
from utils.common import BaseModel
from django.utils.html import format_html


class Posts(BaseModel):
    """
    This model represents the posts table in the database
    """

    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    front_page = models.TextField(default="")
    preview_text = models.TextField(default="")
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_articles",
        to_field="username",
        db_column="author",
    )

    class Meta:
        db_table = "posts"
        verbose_name = "Article"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]


class Likes(BaseModel):
    """
    This model represents the likes table in the database. Likes for posts
    """

    post_id = models.ForeignKey(
        Posts,
        db_column="post_id",
        on_delete=models.CASCADE,
        related_name="post_likes",
        to_field="post_id",
    )
    username = models.ForeignKey(
        "users.User",
        db_column="username",
        on_delete=models.CASCADE,
        related_name="user_likes",
        to_field="username",
    )

    class Meta:
        db_table = "likes"
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        constraints = [
            models.UniqueConstraint(
                fields=["post_id", "username"],
                name="unique_like_post_user",
            )
        ]


class Comments(BaseModel):
    """
    This model represents the comments table in the database. Comments for posts
    """

    comment_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(
        Posts,
        db_column="post_id",
        on_delete=models.CASCADE,
        related_name="article_comments",
        to_field="post_id",
    )
    username = models.ForeignKey(
        "users.User",
        db_column="user_id",
        on_delete=models.CASCADE,
        related_name="user_comments",
        to_field="username",
    )
    comment = models.TextField()

    class Meta:
        db_table = "comments"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["comment_id"]


class Images(BaseModel):
    """
    This model represents the images tables in the database
    """

    image_id = models.AutoField(primary_key=True)
    image = models.TextField()
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def normalize_image(self):
        if self.image:
            return format_html(f'<img src="{self.image}" width="100" height="100" />')
        return ""

    class Meta:
        db_table = "images"
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ["image_id"]


class PostImages(BaseModel):
    """
    This model represents the relationship between posts and images
    """

    image_id = models.ForeignKey(
        Images,
        db_column="image_id",
        on_delete=models.CASCADE,
        related_name="article_images",
        to_field="image_id",
    )
    post_id = models.ForeignKey(
        Posts,
        db_column="post_id",
        on_delete=models.CASCADE,
        related_name="article_images",
        to_field="post_id",
    )

    class Meta:
        db_table = "post_images"
        verbose_name = "Post Image"
        verbose_name_plural = "Posts Images"
        ordering = ["image_id"]


class SavedPosts(BaseModel):
    """
    This model represents the saved posts table in the database
    """

    post_id = models.ForeignKey(
        Posts,
        db_column="post_id",
        on_delete=models.CASCADE,
        related_name="saved_posts",
        to_field="post_id",
    )
    username = models.ForeignKey(
        "users.User",
        db_column="username",
        on_delete=models.CASCADE,
        related_name="user_saved_posts",
        to_field="username",
    )

    class Meta:
        db_table = "saved_posts"
        verbose_name = "Saved Post"
        verbose_name_plural = "Saved Posts"
        constraints = [
            models.UniqueConstraint(
                fields=["post_id", "username"],
                name="unique_saved_post_user",
            )
        ]
        ordering = ["-created_at"]


class BloquedAuthor(BaseModel):
    """
    This model represents the blocked authors table in the database
    """

    author = models.ForeignKey(
        "users.User",
        db_column="author",
        on_delete=models.CASCADE,
        related_name="blocked_authors",
        to_field="username",
    )
    username = models.ForeignKey(
        "users.User",
        db_column="username",
        on_delete=models.CASCADE,
        related_name="blocked_by",
        to_field="username",
    )
    reason = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "blocked_authors"
        verbose_name = "Blocked Author"
        verbose_name_plural = "Blocked Authors"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "username"],
                name="unique_blocked_author_user",
            )
        ]
        ordering = ["-created_at"]
