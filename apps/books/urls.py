from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add$', views.add, name='add'),
    url(r'^process_book$', views.process_book, name='process_book'),
    url(r'^(?P<id>[0-9]+)/$', views.display_book, name='display_book'),
    url(r'^delete_review/(?P<id>[0-9]+)/$', views.delete_review, name='delete_review')
]