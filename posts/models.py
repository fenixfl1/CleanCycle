from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from utils.common import BaseModel
from django.utils.html import format_html


class Likes(BaseModel):
    """
    This model represents the likes table in the database. Likes for posts
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_likes",
        to_field="username",
        db_column="user",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self) -> str:
        return f"{self.user.username} - {self.content_type.model} - {self.object_id}"

    def __repr__(self) -> str:
        return f"{self.user.username} - {self.content_type.model} - {self.object_id}"

    def normalize_user(self):
        return format_html(f"{self.user.username}")

    def normalize_content_type(self):
        return format_html(f"{self.content_type.model}")

    def normalize_object_id(self):
        return format_html(f"{self.object_id}")

    normalize_user.short_description = "User"
    normalize_content_type.short_description = "Content Type"
    normalize_object_id.short_description = "Object ID"

    class Meta:
        db_table = "likes"
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        constraints = [
            models.UniqueConstraint(
                fields=["content_type", "user", "object_id"],
                name="unique_like_content_type_object_user",
            )
        ]


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

    def __str__(self) -> str:
        return f"{self.post_id} - {self.title}"

    def __repr__(self) -> str:
        return f"{self.post_id} - {self.title}"

    def normalize_content(self):
        return format_html(f"{self.content[:100]}...")

    def normalize_title(self):
        return format_html(f"{self.title[:50]}...")

    def normalize_author(self):
        return format_html(f"{self.author.username}")

    def normalize_front_page(self):
        return format_html(f"<img src='{self.front_page}' width='100' height='100' />")

    def get_likes(self):
        """
        This method return the list of usernames that liked the post and the count of likes
        """
        post_content_type = ContentType.objects.get_for_model(self)
        likes = Likes.objects.filter(
            content_type=post_content_type, object_id=self.post_id
        )

        count = likes.count()

        # Obtener la lista de nombres de usuario que dieron like
        liked_usernames = [like.user.username for like in likes]

        return (liked_usernames, count)

    def like_post(self, user):
        """
        This method allows to like a post
        """
        post_content_type = ContentType.objects.get_for_model(self)
        like = Likes.objects.create(
            user=user, content_type=post_content_type, object_id=self.post_id
        )
        return like

    normalize_content.short_description = "Content"
    normalize_title.short_description = "Title"
    normalize_author.short_description = "Author"
    normalize_front_page.short_description = "Front Page"


class Comments(BaseModel):
    """
    This model represents the comments table in the database. Comments for posts
    """

    comment_id = models.AutoField(primary_key=True)
    comment = models.TextField()

    class Meta:
        db_table = "comments"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["comment_id"]


class CommentXPost(BaseModel):
    """
    This model represents the relationship between posts and comments
    `TABLE`: comment_x_post
    """

    comment_id = models.ForeignKey(
        Comments,
        db_column="comment_id",
        on_delete=models.CASCADE,
        related_name="comment_posts",
        to_field="comment_id",
    )
    post_id = models.ForeignKey(
        Posts,
        db_column="post_id",
        on_delete=models.CASCADE,
        related_name="comment_posts",
        to_field="post_id",
    )

    class Meta:
        db_table = "comment_x_post"
        verbose_name = "Comment X Post"
        verbose_name_plural = "Comments X Posts"
        ordering = ["comment_id"]

    def __str__(self) -> str:
        return f"{self.comment_id} - {self.post_id}"

    def __repr__(self) -> str:
        return f"{self.comment_id} - {self.post_id}"

    def normalize_comment(self):
        return format_html(f"{self.comment_id.comment[:50]}...")

    def normalize_post(self):
        return format_html(f"{self.post_id.title[:50]}...")

    normalize_comment.short_description = "Comment"
    normalize_post.short_description = "Post"


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
