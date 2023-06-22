from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('login', views.login_page, name='login_page'),
    path('logout', views.logout_page, name='logout_page')
]
