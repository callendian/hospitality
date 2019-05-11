from django.contrib import admin
from main.models import Guide, Tours, Review, Countries, States, Cities, Visitors, VisitorReview

class GuideAdmin(admin.ModelAdmin):
    pass

class ToursAdmin(admin.ModelAdmin):
    pass

class CountriesAdmin(admin.ModelAdmin):
    pass

class StatesAdmin(admin.ModelAdmin):
    pass

class CitiesAdmin(admin.ModelAdmin):
    pass

class VisitorsAdmin(admin.ModelAdmin):
    pass

class VisitorReviewAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Guide, GuideAdmin)
admin.site.register(Tours, ToursAdmin)
admin.site.register(Countries, CountriesAdmin)
admin.site.register(Cities, CitiesAdmin)
admin.site.register(Visitors, VisitorsAdmin)
admin.site.register(VisitorReview, VisitorReviewAdmin)