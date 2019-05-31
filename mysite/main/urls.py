from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('guides', views.guides, name='guides'),
    path('reviews/guide/<int:guide_id>', views.guide_reviews, name='guide_reviews'),
    path('reviews/visitor/<int:visitor_id>', views.visitor_reviews, name='visitor_reviews'),
    path('tours/<int:id>', views.tours, name='tours'), 
    path('search/', views.search, name='search'), 
    path('saved/', views.saved, name='saved'), 
    path('requested/', views.requested, name='requested')
] 