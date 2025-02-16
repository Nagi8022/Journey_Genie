from django.contrib import admin

from .models import PlacesModel,UsersModel,CartModel,BookingModel

admin.site.register(PlacesModel)
admin.site.register(UsersModel)
admin.site.register(CartModel)
admin.site.register(BookingModel)