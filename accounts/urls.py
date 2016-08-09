from django.conf.urls import url
from . import views, models
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_success/$', views.register_success),
    url(r'^login/$', login),
    url(r'^auth/$', views.auth_view),
    url(r'^loggedin/$', views.loggedin),
    url(r'^logged_out/$', logout),
]
