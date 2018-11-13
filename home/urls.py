from django.conf.urls import url
from . import views as home_views

urlpatterns = [
    url(r'^$', home_views.homepage, name='homepage'),
    url(r'^introduce/$', home_views.introduce, name='introduce'),
    url(r'^accounts/signup/$',home_views.signup, name='signup'),
    url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        home_views.activate, name='activate'),
]
