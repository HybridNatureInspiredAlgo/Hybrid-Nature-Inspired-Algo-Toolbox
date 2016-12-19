from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^run', views.run, name='run'),
]