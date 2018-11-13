from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^idea/list/$', views.idea_list, name='idea_list'),
    url(r'^idea/(?P<pk>\d+)/$', views.idea_detail, name='idea_detail'),
    url(r'^idea/new/$', views.idea_new, name='idea_new'),
    url(r'^idea/(?P<pk>\d+)/edit/$', views.idea_edit, name='idea_edit'),
    url(r'^idea/(?P<pk>\d+)/delete/$', views.idea_delete, name='idea_delete'),
    url(r'^idea/(?P<pk>\d+)/comment/$', views.add_comment_to_idea, name='add_comment_to_idea'),
]
    
