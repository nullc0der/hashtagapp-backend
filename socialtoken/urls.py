from django.urls import path

from socialtoken import views

urlpatterns = [
    path('twitter/getrequesttoken/', views.GetTwitterRequestToken.as_view()),
    path('twitter/getusertoken/', views.GetTwitterUserToken.as_view()),
    path('twitter/deleteusertoken/', views.DeleteTwitterUserToken.as_view())
]
