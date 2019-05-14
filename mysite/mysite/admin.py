from django.contrib import admin
from main.models import Guide, Review, Tours

class GuideAdmin(admin.ModelAdmin):
    pass

class ToursAdmin(admin.ModelAdmin):
    pass

class ReviewAdmin(admin.ModelAdmin):
    pass

admin.site.register(Guide, GuideAdmin)
admin.site.register(Tours, ToursAdmin)
admin.site.register(Review, ReviewAdmin)