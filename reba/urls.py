from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='reba-home'),
    path('about/', views.about, name='reba-about'),
    path('rebaWithoutVideo/', views.rebaWithoutVideo, name='reba-rebaWithoutVideo'),
    path('rebaWithVideo/', views.rebaWithVideo, name='reba-rebaWithVideo'),
    path('rebaResults/', views.rebaResults, name='reba-results'),
    path('export/xls/', views.export_users_xls, name='export_users_xls'),
]
