from django.db import models
from django.contrib.auth.models import User


class Timestamp(models.Model):
    
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class UserProfile(Timestamp):
    DEFAULT_PIC_URL = "https"
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name="profile")
    pofile_pic_url = models.CharField(max_length=255, default=DEFAULT_PIC_URL)
    bio = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)


class NetworkEdge(Timestamp):
    from_user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name="followwing")
    to_user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name="followers")

    class Meta:
        unique_together = ('from_user', 'to_user')