from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('visitor/', views.visitor, name='visitor'),
    path('guide/', views.guide, name='guide'),
    path('tour/', views.create_tour, name='create_tour'),
    path('saved/', views.saved, name='saved'),
    path('tours/all', views.all_tours, name='all_tours'),
    path('tour/<int:id>/', views.tour, name='tour_specific'),
    path('request/<int:t_id>/', views.request_tour, name='request_tour'), 
    path('requested/', views.requested, name='requested')
] 
