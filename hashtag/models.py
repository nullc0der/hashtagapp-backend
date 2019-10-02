import os

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete


class HashtagImage(models.Model):
    image = models.ImageField(upload_to='hashtag_images')
    uid = models.CharField(max_length=12, default='')


@receiver(post_delete, sender=HashtagImage)
def remove_user_hashtag_image(sender, **kwargs):
    instance = kwargs['instance']
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
