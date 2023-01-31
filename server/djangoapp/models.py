from django.db import models
from django.core import serializers
from django.utils.timezone import now
import uuid
import json

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.CharField(max_length=100)
    type = models.CharField(
        max_length=10,
        choices=[("SEDAN", "Sedan"), ("SUV", "SUV"), ("WAGON", "Wagon"), ("TRUCK", "Truck")]
    )
    year = models.IntegerField()

    def __str__(self):
        return f"{self.make} - {self.name}"

class CarDealer:
    def __init__(self, dealer_id, name, address):
        self.dealer_id = dealer_id
        self.name = name
        self.address = address

class DealerReview:
    def __init__(self, dealer_id, rating, review, reviewer_name):
        self.dealer_id = dealer_id
        self.rating = rating
        self.review = review
        self.reviewer_name = reviewer_name
