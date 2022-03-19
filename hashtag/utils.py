import subprocess
import os
import base64
from urllib.parse import unquote

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
        me = api.verify_credentials()
        profile_image = me.profile_image_url_https
        return get_full_size_twitter_image_url(profile_image)
    except TwitterToken.DoesNotExist:
        return ''


def convert_svg_to_png(svg_string: str) -> str:
    filename = get_random_string(length=24)
    with open(f'/tmp/{filename}.svg', 'w+') as svgfile:
        svgfile.write(unquote(svg_string))
    inkscape_path_result = subprocess.run(
        ['which', 'inkscape'], capture_output=True)
    subprocess.run([
        inkscape_path_result.stdout.strip(),
        '--export-filename',
        f'/tmp/{filename}.png',
        '-w', '600', '-h', '600',
        f'/tmp/{filename}.svg'], capture_output=True)
    with open(f'/tmp/{filename}.png', "rb") as pngfile:
        img_string = f'data:image/png;base64,{base64.b64encode(pngfile.read()).decode("utf-8")}'
    os.remove(f'/tmp/{filename}.svg')
    os.remove(f'/tmp/{filename}.png')
    return img_string
