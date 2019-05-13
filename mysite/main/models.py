from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.utils import timezone

# Create your models here.

class Guide(models.Model):
    name = models.CharField('name', max_length=22)
    description = models.CharField('description', max_length=250)
    createdAt = models.DateTimeField('date created', default=datetime.datetime.now())
    editedAt = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

class Tours(models.Model):
    Guest = models.ForeignKey(User, on_delete=models.CASCADE)
    Guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    Start = models.DateTimeField('start_time')
    End = models.DateTimeField('end_time')
    createdAt = models.DateTimeField('date created', default=datetime.datetime.now())
    editedAt = models.DateTimeField(auto_now=True)
    notesToGuide = models.CharField('description', null=True, max_length=500, unique=False)
    def save(self, *args, **kwargs):
        # check for time conflicts, i.e. if the guide has any other tours scheduled for that time
        scheduled_tours = Tours.objects.filter(Guide=self.Guide, Start_date__range=(self.Start, self.End), End_date__range=(self.Start, self.End))
        if not scheduled_tours:
            return
        super().save(*args, **kwargs)
    

class Review(models.Model):
    # only one review per Tour allowed
    Tour = models.ForeignKey(Tours, on_delete=models.CASCADE, unique=True)
    title = models.CharField(null=True, max_length=50)
    content = models.CharField('description', max_length=500)
    STAR_RATING = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    stars = models.CharField(max_length=2, choices=STAR_RATING)
    createdAt = models.DateTimeField('date created', default=datetime.datetime.now())
    editedAt = models.DateTimeField(auto_now=True)


    #edit save to make sure only one review is allowed per person per guide

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
    description = models.CharField('description', max_length=250)
    createdAt = models.DateTimeField('date created', default=datetime.datetime.now())
    editedAt = models.DateTimeField(auto_now=True)
    choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    sex = models.CharField(max_length=10, choices=choices)
    tour = models.ManyToManyField(Tours)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class VisitorReview(models.Model):
    visitor = models.ForeignKey(Visitors, on_delete=models.CASCADE, unique=True)
    title = models.CharField(null=True, max_length=50)
    content = models.CharField('description', max_length=500)
    STAR_RATING = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    stars = models.CharField(max_length=2, choices=STAR_RATING)
    createdAt = models.DateTimeField('date created', default=datetime.datetime.now())
    editedAt = models.DateTimeField(auto_now=True)

class Disputes(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, unique=True)
    visitor = models.ForeignKey(Visitors, on_delete=models.CASCADE, unique=True)
    description = models.CharField("description", max_length=500)
    createdAt = models.DateTimeField('date created', default=datetime.datetime.now())
    editedAt = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if(len(self.description) < 5):
            return "Enter a longer valid description"
        super().save(*args, **kwargs)


