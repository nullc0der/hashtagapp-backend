from django.urls import path

from hashtag import views

urlpatterns = [
    path('getnonexistentphoto/', views.get_non_existent_photo),
    path('downloadsocialimage/', views.DownloadSocialPhotoView.as_view()),
    path('uploadimage/', views.UploadHashtagImageView.as_view())
]
