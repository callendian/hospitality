from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import VisitorReview, Visitors, Cities, States, Countries, Review, Tours, Guide

class touristReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorReview
        fields = ('visitor', 'title', 'content', 'stars', 'createdAt', 'editedAt')

