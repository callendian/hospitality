import csv
from main.models import Country

with open('webscrape/countries_webscrape.csv') as csvfile:
    csv_file = csv.DictReader(csvfile)
    i = 0
    for row in csv_file:
        country_result = Country(name=row['name'], code=i)
        country_result.save()
        i += 1