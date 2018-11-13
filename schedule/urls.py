from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.schedule_list, name='schedule_list'),
    url(r'^reserve/$', views.schedule_reserve, name='schedule_reserve'),
]