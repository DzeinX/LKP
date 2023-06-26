from django.urls import path
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    path('main', views.main, name='main'),
    path('home', views.home, name='home'),
    path('base_template', views.base_template, name='base_template'),
    path('app', views.app, name='app'),
    path('login_page', views.login_page, name='login_page'),
    path('create', views.create, name='create'),
    path('critery', views.critery, name='critery'),
    path('critery_category', views.critery_category, name='critery_category'),
    path('edit', views.edit, name='edit'),
    path('edit_add', views.edit_add, name='edit_add'),
    path('efficiency', views.efficiency, name='efficiency'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('report', views.report, name='report'),
    path('show', views.show, name='show')
]
