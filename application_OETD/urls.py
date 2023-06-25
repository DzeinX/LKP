from django.urls import path
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('', views.main, name='home'),
    path('', views.main, name='baseTemplate'),
    path('', views.main, name='app'),
    path('', views.main, name='loginPage'),
    path('', views.main, name='create'),
    path('', views.main, name='critery'),
    path('', views.main, name='criteryCategory'),
    path('', views.main, name='edit'),
    path('', views.main, name='editAdd'),
    path('', views.main, name='efficiency'),
    path('', views.main, name='portfolio'),
    path('', views.main, name='report'),
    path('', views.main, name='show')
]
