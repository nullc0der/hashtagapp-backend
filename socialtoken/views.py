from rest_framework import views, status
from rest_framework.response import Response

from socialtoken.models import TwitterToken
from socialtoken.utils import (
    get_twitter_request_token, get_twitter_user_auth_token)


class GetTwitterRequestToken(views.APIView):
    """
    This view will be used for getting a request token from twitter
    """

    def post(self, request, format=None):
        res = get_twitter_request_token()
        if res.status_code == 200:
            data = {}
            for d in res.content.decode('utf-8').split('&'):
                key, val = d.split('=')
                data[key] = val
            return Response(data)
        return Response(
            {'error': 'Server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTwitterUserToken(views.APIView):
    """
    This view will be used to get user access token and secret from twitter
    """

    def post(self, request, format=None):
        res = get_twitter_user_auth_token(
            request.query_params['oauth_token'],
            request.query_params['oauth_verifier'])
        if res.status_code == 200:
            twittertoken = TwitterToken()
            for d in res.content.decode('utf-8').split('&'):
                key, val = d.split('=')
                if key == 'oauth_token':
                    twittertoken.oauth_token = val
                if key == 'oauth_token_secret':
                    twittertoken.oauth_token_secret = val
                twittertoken.save()
            return Response({'success': True, 'uid': twittertoken.uid})
        return Response(
            {'error': 'Server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class DeleteTwitterUserToken(views.APIView):
    """
    This view will be used to delete twitter user token
    """

    def post(self, request, format=None):
        try:
            twittertoken = TwitterToken.objects.get(id=request.data['uid'])
            twittertoken.delete()
            return Response({'success': True})
        except TwitterToken.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
