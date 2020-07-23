from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^api/users/(?P<pk>[0-9]+)$', views.UserView.as_view()),
    url(r'^api/users/$', views.UserView.as_view()),
    url(r'^api/users/create/$', views.UserCreateView.as_view()),
    url(r'^api/users/login/$', views.UserLoginView.as_view()),
    url(r'^api/users/logout/$', views.UserLogoutView.as_view()),
    url(r'^api/users/password/change/$',
        views.UserPasswordChangeView.as_view()),
    url(r'^api/users/friends/(?P<username>[a-zA-Z0-9]+)$',
        views.UserFriendsView.as_view()),
    url(r'^api/users/friends/$',
        views.UserFriendsView.as_view()),
    url(r'^api/users/friends/requests/$',
        views.UserFriendsRequestView.as_view()),
]
