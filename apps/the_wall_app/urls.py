from django.conf.urls import url
from . import views

urlpatterns = [
    # root goes to the index
    url(r'^$', views.index),

]