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
        return str(self.year.strftime("%Y")) + ' ' + self.name + ' ' + self.get_trim_display() + ' ' + self.get_type_display()

# <HINT> Create a plain Python class `CarDealer` to hold dealer data

# <HINT> Create a plain Python class `DealerReview` to hold review data
