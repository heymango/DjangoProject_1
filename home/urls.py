from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('home/mypage/', views.mypage, name='home'),
]

