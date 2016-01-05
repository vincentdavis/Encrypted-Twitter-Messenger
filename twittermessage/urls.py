from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^twitterapi/$', views.twitterapi),
    url(r'^account/$', views.user_account),

    
    
]