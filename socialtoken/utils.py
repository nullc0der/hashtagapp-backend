import requests
from requests_oauthlib import OAuth1

from django.conf import settings


def get_twitter_request_token():
    callback_uris = {
        'local': 'http://localhost:3000/twicallback/',
        'production': 'https://hashtag.baza.foundation/twicallback/',
        'beta': 'https://hashtag.baza.foundation/twicallback/'
    }
    auth = OAuth1(
        callback_uri=callback_uris[settings.SITE_TYPE],
        client_key=settings.TWITTER_KEY,
        client_secret=settings.TWITTER_SECRET
    )
    res = requests.post(
        'https://api.twitter.com/oauth/request_token', auth=auth)
    return res


def get_twitter_user_auth_token(oauth_token, oauth_verifier):
    auth = OAuth1(
        client_key=settings.TWITTER_KEY,
        client_secret=settings.TWITTER_SECRET,
        resource_owner_key=oauth_token
    )
    data = {
        'oauth_verifier': oauth_verifier
    }
    res = requests.post(
        'https://api.twitter.com/oauth/access_token?oauth_verifier',
        data=data,
        auth=auth
    )
    return res
