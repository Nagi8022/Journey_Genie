from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('search/', views.search_destinations, name='search_destinations'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('homes/', views.homes, name='homes'),
    path('addplaces/', views.addplaces, name='addplaces'),
    path('destdetails/<int:id>/', views.destdetails, name='destdetails'),
    path('addsubplaces/<int:id>/', views.addsubplaces, name='addsubplaces'),
    path('addfoods/<int:id>/', views.addfoods, name='addfoods'),

    path('addrooms/<int:id>/', views.addrooms, name='addrooms'),
    path('updateplace/<int:id>/<int:jid>/',
         views.updateplace, name='updateplace'),
    path('deleteplace/<int:id>/<int:jid>/',
         views.deleteplace, name='deleteplace'),
    path('updatefoods/<int:id>/<int:jid>/',
         views.updatefoods, name='updatefoods'),
    path('deletefoods/<int:id>/<int:jid>/',
         views.deletefoods, name='deletefoods'),
    path('updaterooms/<int:id>/<int:jid>/',
         views.updaterooms, name='updaterooms'),
    path('deleterooms/<int:id>/<int:jid>/',
         views.deleterooms, name='deleterooms'),
    path('roomsingledest/<int:id>/<int:jid>/',
         views.roomsingledest, name='roomsingledest'),
    path('foodsingledest/<int:id>/<int:jid>/',
         views.foodsingledest, name='foodsingledest'),
    path('placesingledest/<int:id>/<int:jid>/',
         views.placesingledest, name='placesingledest'),
    path('destinations/', views.destinations, name="destinations"),
    path('filter/', views.filter, name='filter'),

    path('cart/', views.cart, name='cart'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('removecart/<int:id>/', views.removecart, name='removecart'),
    path('booknow/<int:id>/', views.booknow, name='booknow'),

    path('logout/', views.logout, name="logout"),
    path('bookings/', views.bookings, name='bookings'),
    path('recommend/', views.recommend, name='recommend'),






]
