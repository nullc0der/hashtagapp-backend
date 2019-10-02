from mimetypes import MimeTypes

import tweepy
from django.utils.crypto import get_random_string
from django.conf import settings

from socialtoken.models import TwitterToken
from hashtag.models import HashtagImage


def get_hashtag_uid():
    uid = get_random_string()
    is_not_unique = HashtagImage.objects.filter(uid=uid).count() > 0
    while is_not_unique:
        get_hashtag_uid()
    return uid


def get_final_file(photo):
    photo_name_splited = photo.name.split('.')
    if not len(photo_name_splited) > 1:
        extension = MimeTypes().guess_extension(photo.content_type)
        photo.name = photo_name_splited[0] + extension
    return photo


def get_full_size_twitter_image_url(url):
    url_chunks = url.split('/')
    filename = url_chunks[len(url_chunks) - 1]
    name, filetype = filename.split('.')
    name_chunks = name.split('_')
    name_chunks.pop(len(name_chunks) - 1)
    full_size_filename = '_'.join(name_chunks) + '.' + filetype
    for i in range(2):
        url_chunks.pop(0)
    url_chunks.pop(len(url_chunks) - 1)
    return 'https://' + '/'.join(url_chunks) + '/' + full_size_filename


def get_facebook_profile_photo(uid):
    return "https://graph.facebook.com" +\
        "/%s/picture?width=9999&height=9999"\
        % uid


def get_twitter_profile_photo(twitter_token_uid):
    try:
        twitter_token = TwitterToken.objects.get(uid=twitter_token_uid)
        auth = tweepy.OAuthHandler(
            settings.TWITTER_KEY,
            settings.TWITTER_SECRET)
        auth.set_access_token(
            twitter_token.oauth_token,
            twitter_token.oauth_token_secret
        )
        api = tweepy.API(auth)
        me = api.me()
        profile_image = me.profile_image_url_https
        return get_full_size_twitter_image_url(profile_image)
    except TwitterToken.DoesNotExist:
        return ''
