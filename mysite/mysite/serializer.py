from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import *

class touristReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorReview
        fields = ('visitor', 'title', 'content', 'stars', 'createdAt', 'editedAt')

