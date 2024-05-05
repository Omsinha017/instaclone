from django.db import models
from users.models import Timestamp, UserProfile


class UserPost(Timestamp):

    caption_text = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True, db_index=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post')
    is_published = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['location', 'created_on'], name="location_creadted_on_idx"),
            models.Index(fields=['location', '-created_on'], name="location_creadted_on_idx_desc"),
        ]

class PostMedia(Timestamp):
    media_file = models.FileField(upload_to='post/media')
    sequence_index = models.PositiveSmallIntegerField(default=0)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='media')

    class Meta:
        unique_together = ('sequence_index', 'post', )

class PostLikes(models.Model):

    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='likes')
    liked_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='liked_posts')

    class Meta:
        unique_together = ('post', 'liked_by', )

class PostComments(models.Model):

    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments_made')

    text = models.CharField(max_length=255)

