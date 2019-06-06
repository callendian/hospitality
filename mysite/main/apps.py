from django.apps import AppConfig
import sys


class MainConfig(AppConfig):
    
    name = 'main'
    def ready(self):
        all_city = ["Seattle", 
        "Portland", 
        "Austin", 
        "Los Angeles", 
        "San Francisco",
        "Dallas",
        "Washington D.C",
        "New York City",
        "Chicago",
        "New Orleans", 
        "Oklahoma City",
        "Boise"]
        City = self.get_model('City')
        if(City.objects.all().count() == 0):
            for city in all_city:

                Country = self.get_model('Country')
                newCity = City()
                newCity.name = city
                newCity.country = Country.objects.get(name="United States")
                try:
                    newCity.save()
                except:
                    print(sys.exc_info()[1])
                    return 
