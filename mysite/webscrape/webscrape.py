# Takes the csv file: countries_webscrape.csv and populates the counties model.
# This code was executed using the django shell.
# Based on code from http://abhishekchhibber.com/django-importing-a-csv-file-to-database-models/
import csv
from main.models import Country

with open('webscrape/countries_webscrape.csv') as webscrapecsv:
    csv_file = csv.DictReader(webscrapecsv)
    i = 0
    for row in csv_file:
        country_result = Country(name=row['name'], code=i)
        country_result.save()
        i += 1