from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

STAR_RATING = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')
)

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'), 
    ('N/A', 'Undisclosed')
)

# Represents a Guide's profile
class Guide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=510, default="")
    email = models.CharField(max_length=254, default="")
    gender = models.CharField(max_length=10, choices=GENDER, default="N/A")
    bio = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField('date created', auto_now_add=True)

    def natural_key(self):
        return (self.first_name, self.last_name)


# Represents a Visitor's profile
class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=510, default="")
    email = models.CharField(max_length=254, default="")
    gender = models.CharField(max_length=10, choices=GENDER, default="N/A")
    createdAt = models.DateTimeField('date created', auto_now_add=True)

    def natural_key(self):
        return (self.first_name, self.last_name)


# Reference table for tour types (general, outdoors, sightseeing, food, etc)
class TourType(models.Model):
    choices = (
        ('General', 'General'),
        ('Food', 'Food'),
        ('Adventure', 'Adventure'),
        ('Shopping', 'Shopping'),
        ('Educational', 'Educational'),
        ('Mixed', 'Mixed')
    )
    name = models.CharField(max_length=50, choices=choices, unique=True)
    description = models.TextField(null=True, blank=True)

    def natural_key(self):
        return (self.name)

# Represents a tour appointment between 1 guide and 1 user
class Tour(models.Model):
    guide = models.ForeignKey('Guide', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="Tour", blank=True)
    tourType = models.ForeignKey('TourType', on_delete=models.CASCADE)
    city = models.ManyToManyField('City')
    description = models.TextField(null=True, blank=True)
    days = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)


# Represents bookmarked/planned tours
class SavedTour(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)


# Request to book
class TourRequest(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.end_date < self.start_date:
            raise ValidationError('End date cannot be before start date')

        # check for time conflicts, i.e. if the guide has any other tours scheduled for that time
        scheduled_tours = Booking.objects.filter(
            tour=self.tour,
            start_date__range=(self.start_date, self.end_date),
            end_date__range=(self.start_date, self.end_date)
        )
        
        if scheduled_tours.exists():
            raise ValidationError('Schedule Conflict')
        super().save(*args, **kwargs)


# Individual appointments of tour guides and visitors
class Booking(models.Model):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)
    '''
    def save(self, *args, **kwargs):
        if self.start_date < self.end_date:
            return 'End date cannot be before start date'

        # check for time conflicts, i.e. if the guide has any other tours scheduled for that time
        scheduled_tours = Booking.objects.filter(
            tour=self.tour,
            start_date__range=(self.start_date, self.end_date),
            end_date__range=(self.start_date, self.end_date)
        )
        if scheduled_tours.exists():
            raise ValidationError('Schedule Conflict')
        super().save(*args, **kwargs)
    '''

# Reviews of visitors towards tours/guides
class TourReview(models.Model):
    # only one review per visitor booking allowed
    reviewer = models.ForeignKey('Visitor', on_delete=models.CASCADE, default=None)
    guide = models.ForeignKey('Guide', on_delete=models.CASCADE, default=None)
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.CharField(max_length=2, choices=STAR_RATING)
    createdAt = models.DateTimeField('date created', auto_now_add=True)
    editedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Checks to make sure that only a visitor can only review a booking once
        reviews = TourReview.objects.filter(
            reviewer=self.reviewer, booking=self.booking)
        if reviews.exists():
            if reviews[0].id != self.pk:
                raise ValidationError('Review already exists')
        super().save(*args, **kwargs)


# Reviews of visitors towards tours/guides
class VisitorReview(models.Model):
    # only one review per tour booking allowed
    reviewer = models.ForeignKey('Guide', on_delete=models.CASCADE, default=None)
    visitor = models.ForeignKey('Visitor', on_delete=models.CASCADE, default=None)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, default=None)
    content = models.TextField()
    rating = models.CharField(max_length=2, choices=STAR_RATING)
    createdAt = models.DateTimeField('date created', auto_now_add=True)
    editedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Checks to make sure that only a visitor can only review a booking once
        reviews = VisitorReview.objects.filter(
            reviewer=self.reviewer, booking=self.booking)
        if reviews.exists():
            if reviews[0].id != self.pk:
                raise ValidationError('Review already exists')
        super().save(*args, **kwargs)


# Disputes on bookings
class Dispute(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, null=True)
    visitor = models.ForeignKey('Visitor', on_delete=models.CASCADE, null=True)
    guide = models.ForeignKey('Guide', on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=500)
    createdAt = models.DateTimeField(auto_now_add=True)
    editedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if(len(self.description) < 5):
            raise ValidationError('Review already exists')
        super().save(*args, **kwargs)



# Reference table for countries
class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(null=True, blank=True, max_length=5)

    class Meta:
        verbose_name_plural = 'countries'


# Reference table for states
class State(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    code = models.CharField(null=True, blank=True, max_length=5)


# Reference table for cities
class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    state = models.ForeignKey('State', on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(null=True, blank=True, max_length=5)

    class Meta:
        verbose_name_plural = 'cities'

    def natural_key(self):
        return (self.name + ', ' + self.country.name)
