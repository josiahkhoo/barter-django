from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)

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
    url(r'^api/users/reverify/$',
        views.UserSendVerificationEmailView.as_view()),
    path('api/users/verify/<uuid:uuid>',
         views.UserVerifyEmailView.as_view()),
    url(r'^api/users/facebook/$',
        views.FacebookLoginView.as_view(), name='fb_login'),
    url(r'^api/users/facebook/connect/$',
        views.FacebookConnectView.as_view(), name='fb_connect'),
    url(r'^api/users/google/$',
        views.GoogleLoginView.as_view(), name='google_login'),
    url(r'^api/users/google/connect/$',
        views.GoogleConnectView.as_view(), name='google_connect'),
]

urlpatterns += [
    url(
        r'^api/users/socialaccounts/$',
        SocialAccountListView.as_view(),
        name='social_account_list'
    ),
    url(
        r'^api/users/socialaccounts/(?P<pk>\d+)/disconnect/$',
        SocialAccountDisconnectView.as_view(),
        name='social_account_disconnect'
    )
]
