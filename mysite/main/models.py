from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

# Represents a Guide's profile
class Guide(models.Model):
    name = models.CharField('name', max_length=22)
    description = models.TextField()
    createdAt = models.DateTimeField('date created', default=datetime.datetime.now())
    editedAt = models.DateTimeField('date edited', null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

# Represents a tour appointment between 1 guide and 1 user
class Tours(models.Model):
    Guest = models.ForeignKey(User, on_delete=models.CASCADE)
    Guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    Start = models.DateTimeField()
    End = models.DateTimeField('end_time')
    createdAt = models.DateTimeField('date created', default=datetime.datetime.now())
    editedAt = models.DateTimeField('date edited', null=True)
    notesToGuide = models.CharField('description', null=True, max_length=500, unique=False)

# Stores all the reviews of the guides
class Review(models.Model):
    # only one review per Tour allowed
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    Guide = models.ForeignKey(Guide, on_delete=models.CASCADE, default=None)
    title = models.CharField(null=True, max_length=200)
    content = models.TextField()
    STAR_RATING = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    stars = models.CharField(max_length=2, choices=STAR_RATING)
    createdAt = models.DateTimeField('date created', default=datetime.datetime.now())
    editedAt = models.DateTimeField('date edited', null=True)

    def save(self, *args, **kwargs):
        # Checks to make sure that only a user can only review a guide once
        user_reviews = Review.objects.filter(Guide=self.Guide, creator=self.creator)
        if user_reviews.exists():
            if user_reviews[0].id != self.pk:
                raise ValidationError("Review already exists")
        super().save(*args, **kwargs)

class Countries(models.Model):
    name = models.CharField(null=True, max_length=50)
    country_code = models.CharField(null=True, max_length=5)

class States(models.Model):
    country_id = models.ForeignKey(Countries, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=50)
    state_code = models.CharField(null=True, max_length=5)

class Cities(models.Model):
    state_id = models.ForeignKey(States, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=50)
    city_code = models.CharField(null=True, max_length=5)

class Visitors(models.Model):
    name = models.CharField('name', max_length=22)
    description = models.CharField('description', max_length=250)
    createdAt = models.DateTimeField('date created', default=datetime.datetime.now())
    editedAt = models.DateTimeField('date edited', null=True)
    choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    sex = models.CharField(max_length=10, choices=choices)
    tour = models.ManyToManyField(Tours)


