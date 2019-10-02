from django.urls import path, include

urlpatterns = [
    path('social/', include('socialtoken.urls')),
    path('hashtag/', include('hashtag.urls'))
]
