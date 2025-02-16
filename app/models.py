from django.db import models
import os




class UsersModel(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=100)
    profile = models.FileField(upload_to=os.path.join('static', 'profiles'))
    otp = models.IntegerField(null=True)

    def __str__(self):
        return self.firstname + " " + self.lastname

    class Meta:
        db_table = "UsersModel"


class PlacesModel(models.Model):
    placename = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    desc = models.TextField()
    image = models.JSONField(default=list, blank=True)
    places = models.JSONField(default=list, blank=True)
    rooms = models.JSONField(default=list, blank=True)
    restaurants = models.JSONField(default=list, blank=True)
    placetype = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.placename

    class Meta:
        db_table = "PlacesModel"


class CartModel(models.Model):
    hotelname = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    desc = models.TextField()
    image = models.FileField(upload_to=os.path.join('static', 'cartimages'))
    email = models.EmailField(null=True)

    def __str__(self):
        return self.hotelname

    class Meta:
        db_table = "CartModel"


class BookingModel(models.Model):
    hotelname = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    desc = models.TextField()
    image = models.FileField(upload_to=os.path.join('static', 'bookingimages'))
    email = models.EmailField(null=True)

    def __str__(self):
        return self.hotelname

    class Meta:
        db_table = "BookingModel"
