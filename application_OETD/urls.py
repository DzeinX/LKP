from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='home')),
    path('home', views.home, name='home'),
    path('create_file', views.create_file, name='create_file'),
    path('checking_questionnaire/<int:_id>', views.checking_questionnaire, name='checking_questionnaire'),
    path('filling_questionnaire/<int:_id>', views.filling_questionnaire, name='filling_questionnaire'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('edit_add', views.edit_add, name='edit_add'),
    path('questionnaire', views.questionnaire, name='questionnaire'),
    path('portfolio/<int:_id>', views.portfolio, name='portfolio'),
    path('report/<int:_id>', views.report, name='report'),
    path('category_for_checking/<int:_id>', views.category_for_checking, name='category_for_checking'),
    path('file_delete/<int:_id>/<int:user_id>', views.file_delete, name='file_delete'),
    path('result_questionnaire/<int:_id>', views.result_questionnaire, name='result_questionnaire')
]
