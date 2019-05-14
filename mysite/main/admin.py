from django.contrib import admin
from main.models import *


class GuideAdmin(admin.ModelAdmin):
    pass


class VisitorAdmin(admin.ModelAdmin):
    pass


class TourTypeAdmin(admin.ModelAdmin):
    pass


class TourAdmin(admin.ModelAdmin):
    pass


class SavedTourAdmin(admin.ModelAdmin):
    pass


class BookingAdmin(admin.ModelAdmin):
    pass


class TourReviewAdmin(admin.ModelAdmin):
    pass


class VisitorReviewAdmin(admin.ModelAdmin):
    pass


class DisputeAdmin(admin.ModelAdmin):
    pass


class TransactionAdmin(admin.ModelAdmin):
    pass


class CountryAdmin(admin.ModelAdmin):
    pass


class StateAdmin(admin.ModelAdmin):
    pass


class CityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Guide, GuideAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(TourType, TourTypeAdmin)
admin.site.register(Tour, TourAdmin)
admin.site.register(SavedTour, SavedTourAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(TourReview, TourReviewAdmin)
admin.site.register(VisitorReview, VisitorReviewAdmin)
admin.site.register(Dispute, DisputeAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
