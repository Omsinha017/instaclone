from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import PostMedia

@receiver(post_save, sender=PostMedia)
def process_media(sender, instance, **kwargs):
    pass