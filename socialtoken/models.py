from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.


def get_uid():
    return get_random_string(length=12, allowed_chars='0123456789')


class TwitterToken(models.Model):
    uid = models.CharField(default=get_uid, max_length=12)
    oauth_token = models.TextField()
    oauth_token_secret = models.TextField()
