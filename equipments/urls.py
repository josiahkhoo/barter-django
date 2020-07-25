from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

app_name = 'equipments'
urlpatterns = [
    url(r'^api/equipments/(?P<pk>[0-9]+)$', EquipmentView.as_view()),
    url(r'^api/equipments/$', EquipmentView.as_view()),
]
