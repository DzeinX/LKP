from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('login', views.login_page, name='login_page')
]
