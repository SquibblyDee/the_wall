from django.conf.urls import url
from . import views

urlpatterns = [
    # root goes to the index
    url(r'^$', views.index),
    url(r'^wall', views.wall),
    url(r'^process_register', views.process_register),
    url(r'^process_login', views.process_login),
    url(r'^process_comment', views.process_comment),

    url(r'^process_post', views.process_post),
    url(r'^logout', views.logout),

]