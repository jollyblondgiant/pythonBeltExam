from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'register$', views.register),
    url(r'dashboard$', views.dashboard),
    url(r'(?P<id>\d+)/edit$', views.editUser),
    url(r'(?P<id>\d+)/update$', views.updateUser),
    url(r'(?P<id>\d+)/postQuote$', views.post),
    url(r'(?P<id>\d+)/userQuotes$', views.showUser),
    url(r'login$', views.login),
    url(r'logout$', views.logout),
    url(r'(?P<id>\d+)/delete$', views.deletepost),
    url(r'likes/(?P<id>\d+)$', views.addLike)

]