from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

class User(AbstractUser):
    phoneNumber = models.CharField(max_length=12, blank=True, null=True)
    profilePicture = models.ImageField(upload_to="PriceProbe/images/", default='PriceProbe/images/default.jpg')

    def __str__(self):
        return self.username
    
class Product(models.Model):
    users = models.ManyToManyField(User, related_name="products", blank=True)
    productHeaderText = models.CharField(max_length=1000, blank=True, null=True)
    productPrice = models.CharField(max_length=1000, blank=True, null=True)
    productLink = models.CharField(max_length=1000, blank=True, null=True)
    productImage = models.CharField(max_length=1000, blank=True, null=True)
    isProductSaved = models.BooleanField(default=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    #create product from
    #also grab product description
    def __str__(self):
        return self.productHeaderText[:20]


class FrequentlyAskedQuestion(models.Model):
    question = models.CharField(max_length=1000, null=True, blank=True)
    answer = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.question[:20]
