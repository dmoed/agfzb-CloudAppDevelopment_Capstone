from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    MODEL_TYPES = (
        ('sa', 'Saloon'),
        ('se', 'Sedan'),
        ('suv', 'SUV'),
        ('wa', 'Wagon')
    )
    MODEL_TRIM = (
        ('ba', 'Base'),
        ('sp', 'Sport'),
        ('lx', 'Luxury'),
    )
    id = models.BigAutoField(primary_key=True)
    manufacturer = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    dealerId = models.IntegerField()
    type = models.CharField(max_length=20, choices=MODEL_TYPES)
    year = models.DateField()
    trim = models.CharField(max_length=20, choices=MODEL_TRIM)

    def __str__(self):
        return str(
            self.year.strftime("%Y")) + ' ' + self.name + ' ' + self.get_trim_display() + ' ' + self.get_type_display()


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, id, lat, long, st, state, zip):
        self.address = address
        self.city = city
        self.id = id
        self.lat = lat
        self.long = long
        self.state = state
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer: " + self.state + " " + self.city + " " + self.address


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, review, purchase, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership,
        self.name = name,
        self.review = review,
        self.purchase = purchase,
        self.purchase_date = purchase_date,
        self.car_make = car_make,
        self.car_model = car_model,
        self.car_year = car_year
        self.sentiment = sentiment,
        self.id = id

    def __str__(self):
        return "Review: " + str(self.review) + " sentient: " + str(self.sentiment)