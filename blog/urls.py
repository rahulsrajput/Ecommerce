from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.index, name='blog'),
    path('<slug:slug>/', views.blogpost, name='blogpost'),
    
] 