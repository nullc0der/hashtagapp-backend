from itertools import zip_longest
import base64

import requests
import tweepy

from django.conf import settings
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string

from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from socialtoken.models import TwitterToken
from hashtag.utils import (
    get_hashtag_uid,
    get_facebook_profile_photo,
    get_twitter_profile_photo,
    convert_svg_to_png)
from hashtag.models import HashtagImage


URL_PROTOCOL = 'http://' if settings.SITE_TYPE == 'local' else 'https://'


class DownloadSocialPhotoView(views.APIView):
    """
    This API is used to download an users current social profile photo
    """

    def get(self, request, format=None):
        if request.query_params['provider'] == 'facebook':
            url = get_facebook_profile_photo(request.query_params['uid'])
        if request.query_params['provider'] == 'twitter':
            url = get_twitter_profile_photo(request.query_params['uid'])
        if url:
            return Response({'success': True, 'url': url})
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class UploadHashtagImageView(views.APIView):
    """
    This API will be used to upload hashtag image to users social account
    """

    def save_hashtag_image(self, request):
        img_string = convert_svg_to_png(request.data['svg'])
        data = ContentFile(base64.b64decode(img_string.split(
            ',')[1]), name=f'fb-{get_random_string(length=12)}.png')
        hashtag_image = HashtagImage(
            image=data,
            uid=get_hashtag_uid()
        )
        hashtag_image.save()
        return Response({
            'url': "{0}{1}/hashtagimage/{2}/".format(
                URL_PROTOCOL,
                settings.HOST_URL,
                hashtag_image.uid
            )
        })

    def upload_photo_to_twitter(self, request):
        try:
            twitter_token = TwitterToken.objects.get(uid=request.data['uid'])
            img_string = convert_svg_to_png(request.data['svg'])
            data = ContentFile(
                base64.b64decode(img_string),
                name=f'twitter-{get_random_string(length=12)}.png')
            hashtag_image = HashtagImage(
                image=data,
                uid=get_hashtag_uid()
            )
            hashtag_image.save()
            auth = tweepy.OAuthHandler(
                settings.TWITTER_KEY, settings.TWITTER_SECRET)
            auth.set_access_token(
                twitter_token.oauth_token, twitter_token.oauth_token_secret)
            api = tweepy.API(auth)
            user = api.update_profile_image(hashtag_image.image.path)
            return Response({
                'success': True,
                'user': user.screen_name,
                'hashtag_image_uid': hashtag_image.uid
            })
        except TwitterToken.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        if request.data['provider'] == 'facebook':
            return self.save_hashtag_image(request)
        if request.data['provider'] == 'twitter':
            return self.upload_photo_to_twitter(request)


def facebook_share_view(request, uid):
    hashtagimage = HashtagImage.objects.get(uid=uid)
    otherimages = HashtagImage.objects.all().exclude(uid=uid).order_by('-id')
    otherimages = otherimages if otherimages.count(
    ) <= 12 else otherimages[0:12]
    otherimages_chunk = list(zip_longest(*[iter(otherimages)]*4))
    return render(
        request,
        'hashtag/fbshare.html',
        {
            'mainimage': hashtagimage,
            'otherimages_chunk': otherimages_chunk,
            'fb_app_id': settings.FACEBOOK_APP_ID,
            'host': '{0}{1}'.format(
                URL_PROTOCOL,
                settings.HOST_URL
            )
        }
    )


@api_view(['GET'])
def get_non_existent_photo(request):
    response = requests.get(
        'https://www.thispersondoesnotexist.com/image?something')
    return Response({
        'image': f'data:{response.headers["Content-Type"]};base64,'
        f'{base64.b64encode(response.content).decode("utf-8")}'
    })


class DownloadImage(views.APIView):
    """
        This view converts a svg image to png
    """

    def post(self, request, format=None):
        img_string = convert_svg_to_png(request.data['svg'])
        return Response({'img': f'data:image/png;base64,{img_string}'})
