from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('guides', views.tourGuides, name='guides'),
    path('reviews/<int:id>', views.reviews, name='reviews'),
    path('tours/<int:id>', views.tours, name='tours')
] 