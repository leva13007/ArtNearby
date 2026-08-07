from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=50, unique= True)
    description = models.TextField()
    phone = models.IntegerField()
    website = models.URLField(max_length=150)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Location(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    address = models.TextField(max_length=150)
    city = models.CharField()
    length = models.FloatField()
    width = models.FloatField()

class Fabticator(models.Model):
    name = models.CharField(max_length=100, unique = True)

class Product(models.Model):
    CATEGORY_CHOICES = [
        ("fine_art", "Fine Art"), #Right what user see
        ("graphic_art", "Graphic Art"),
        ("papeterie", "Papeterie"),
        ("art_craft", "Art Craft")
    ]


    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.FloatField()
    description = models.TextField()
    fabricator = models.ManyToManyField(Fabticator)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='product_images/',  # Images will save in MEDIA_ROOT/product_images/
        blank=True,               
        null=True                   
    )

    def get_absolute_url(self):
        return reverse('find_it:list-product', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name