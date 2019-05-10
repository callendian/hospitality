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
    editedAt = models.DateTimeField('date edited', null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

class Tours(models.Model):
    Guest = models.ForeignKey(User, on_delete=models.CASCADE)
    Guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    Start = models.DateTimeField()
    End = models.DateTimeField('end_time')
    createdAt = models.DateTimeField('date created', default=datetime.datetime.now())
    editedAt = models.DateTimeField('date edited', null=True)
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
    editedAt = models.DateTimeField('date edited', null=True)

    #edit save to make sure only one review is allowed per person per guide
