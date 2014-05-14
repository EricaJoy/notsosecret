from django.conf.urls import patterns, url

from secretkeeper import views

urlpatterns = patterns('',
    url(r'^vote/', views.vote, name='vote'),
    url(r'^$', views.index, name='index'),

    # Makes the paginated urls pretty
    url(r'/(?P<page>\d+)/$', views.index),
    
)