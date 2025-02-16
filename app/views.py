import random
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
from django.conf import settings
import os
from .models import PlacesModel
from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *



def index(request):
    places = PlacesModel.objects.all()
    return render(request, 'index.html', {'places': places})


def about(request):
    return render(request, 'about.html')


def dest(request):
    dest = PlacesModel.objects.all()
    return render(request, 'desttt.html', {'data': dest})


def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phone = request.POST['contactnumber']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        address = request.POST['address']
        profile = request.FILES['image']
        if password == confirmpassword:
            user = UsersModel.objects.filter(email=email).exists()
            if user:
                messages.error(request, 'User already exists!')
                return redirect('register')
            else:
                user = UsersModel.objects.create(
                    firstname=firstname, lastname=lastname,
                    phone=phone, email=email, password=password, address=address,
                    profile=profile

                )
                user.save()
                messages.success(request, 'User registered successfully!')
                return redirect('register')
        else:
            messages.success(
                request, 'Password and Confirm Password or not matched!')
            return redirect('register')
    return render(request, 'register.html')

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PlacesModel, UsersModel, CartModel, BookingModel

def search_destinations(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        
       
        destinations = PlacesModel.objects.filter(
            Q(placename__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(state__icontains=search_query) |
            Q(placetype__icontains=search_query)
        )
        
        if destinations:
            return render(request, 'desttt.html', {'data': destinations})
        else:
            return render(request, 'desttt.html', {'data': None})
    
 
    destinations = PlacesModel.objects.all()
    return render(request, 'desttt.html', {'data': destinations})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == 'admin@gmail.com' and password == 'admin@12':
            request.session['login'] = 'admin'
            request.session['email'] = email
            return redirect('homes')

        elif UsersModel.objects.filter(email=email, password=password).exists():
            request.session['login'] = 'user'
            request.session['email'] = email
            return redirect('homes')
        else:
            messages.error(request, 'Invalid email or password!')
            return redirect('login')
    return render(request, 'login.html')


def homes(request):
    places = PlacesModel.objects.all()
    login = request.session['login']


    limited_places = places[:6]  # First 6 places

    return render(request, 'homes.html', {
        'login': login,
        'places': limited_places
    })


def home(request):
    places = PlacesModel.objects.all()

    login = request.session['login']
    return render(request, 'homes.html', {'login': login, 'places': places})


def logout(request):
    del request.session['login']
    del request.session['email']
    return redirect('index')


def addplaces(request):
    # PlacesModel.objects.all().delete()
    login = request.session.get('login', None)  
    if request.method == 'POST':
        name = request.POST['name']
        state = request.POST['state']
        desc = request.POST['desc']
        city = request.POST['city']
        image = request.FILES['image']
        areatype = request.POST['areatype']

      
        image_paths = []

        places_images_dir = os.path.join(
            settings.BASE_DIR, 'static', 'places_images')
      
        os.makedirs(places_images_dir, exist_ok=True)

      
        image_path = os.path.join('static/places_images/', image.name)
        print(image_path)
      
        with open(os.path.join(places_images_dir, image.name), 'wb') as img_file:
            for chunk in image.chunks():
                img_file.write(chunk)

         
        image_paths.append({'imgpath': image_path})

     
        place = PlacesModel.objects.create(
            placename=name, state=state, desc=desc, city=city, image=image_paths, placetype=areatype
        )
        place.save()

        messages.success(request, 'Tourism Place added successfully!')
        return redirect('addplaces') 

    return render(request, 'addplaces.html', {'login': login})


def destdetails(request, id):
    login = request.session['login']
    place = PlacesModel.objects.filter(id=id)
    places = PlacesModel.objects.all()
    return render(request, 'destination_details.html', {'place': place, 'login': login, 'places': places})


def addsubplaces(request, id):
    login = request.session['login']
    place = PlacesModel.objects.get(id=id)

    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        location = request.POST['location']
        image = request.FILES['image']
      
        places_images_dir = os.path.join(
            settings.BASE_DIR, 'static', 'places_images')
    
        os.makedirs(places_images_dir, exist_ok=True)

      
        image_path = os.path.join('static/places_images/', image.name)
        print(image_path)
     
        with open(os.path.join(places_images_dir, image.name), 'wb') as img_file:
            for chunk in image.chunks():
                img_file.write(chunk)

          
        place.places.append(
            {'placename': name, 'location': location, 'desc': desc, 'img': image_path})

        place.save()

        messages.success(request, 'Tourism Place added successfully!')
        return redirect('addsubplaces', id)

    return render(request, 'addsubplaces.html', {'login': login, 'id': id})


def addfoods(request, id):
    login = request.session['login']
    place = PlacesModel.objects.get(id=id)

    if request.method == 'POST':
        restname = request.POST['restname']
        name = request.POST['name']
        desc = request.POST['desc']
        location = request.POST['location']
        image = request.FILES['image']
       
        places_images_dir = os.path.join(
            settings.BASE_DIR, 'static', 'places_images')

        os.makedirs(places_images_dir, exist_ok=True)

        
        image_path = os.path.join('static/places_images/', image.name)
        print(image_path)
      
        with open(os.path.join(places_images_dir, image.name), 'wb') as img_file:
            for chunk in image.chunks():
                img_file.write(chunk)

          
        place.restaurants.append({'restname': restname, 'foodname': name,
                                 'location': location, 'desc': desc, 'img': image_path})
        place.save()

        messages.success(request, 'Food or Restaurent added successfully!')
        return redirect('addfoods', id)
    return render(request, 'addfoods.html', {'login': login, 'id': id})


def updateplace(request, id, jid):
    login = request.session['login']
    place = PlacesModel.objects.get(id=id)
    data = place.places[int(jid-1)]
    print(data)
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        location = request.POST['location']
        if 'image' in request.FILES:
            print('==================')
            image = request.FILES['image']
            data['placename'] = name
            data['desc'] = desc
            data['location'] = location
         
            places_images_dir = os.path.join(
                settings.BASE_DIR, 'static', 'places_images')
            
            os.makedirs(places_images_dir, exist_ok=True)
       
            image_path = os.path.join(
                'static/places_images/', image.name)  # Path relative
          
            with open(os.path.join(places_images_dir, image.name), 'wb') as img_file:
                for chunk in image.chunks():
                    img_file.write(chunk)
            print(image_path)
            data['img'] = image_path
            # del data['image']
            place.save()
        else:
            data['placename'] = name
            data['desc'] = desc
            data['location'] = location
            place.save()

        messages.success(request, 'Place Updated Successfully!')
        return redirect('updateplace', id, jid)

    return render(request, 'updateplace.html', {'login': login, 'id': id, 'jid': jid, 'data': data})


def deleteplace(request, id, jid):
    login = request.session['login']
    place = PlacesModel.objects.get(id=id)
    data = place.places
    del data[int(jid-1)]

    place.save()
    messages.success(request, 'Place Deleted Successfully!')
    return redirect('destdetails', id)


def updatefoods(request, id, jid):
    login = request.session['login']
    food = PlacesModel.objects.get(id=id)
    data = food.restaurants[int(jid-1)]
    if request.method == 'POST':
        restname = request.POST['restname']
        name = request.POST['name']
        desc = request.POST['desc']
        location = request.POST['location']
        if 'image' in request.FILES:
            print('==================')
            image = request.FILES['image']
            data['restname'] = restname
            data['foodname'] = name
            data['desc'] = desc
            data['location'] = location

            image = request.FILES['image']
          
            places_images_dir = os.path.join(
                settings.BASE_DIR, 'static', 'places_images')
           
            os.makedirs(places_images_dir, exist_ok=True)

           
            image_path = os.path.join('static/places_images/', image.name)
            print(image_path)
           
            with open(os.path.join(places_images_dir, image.name), 'wb') as img_file:
                for chunk in image.chunks():
                    img_file.write(chunk)

            data['img'] = image_path
            food.save()
        else:
            data['restname'] = restname
            data['foodname'] = name
            data['desc'] = desc
            data['location'] = location
            food.save()

        messages.success(request, 'Food Updated Successfully!')
        return redirect('updatefoods', id, jid)
    return render(request, 'updatefoods.html', {'login': login, 'id': id, 'jid': jid, 'data': data})


def deletefoods(request, id, jid):
    login = request.session['login']
    food = PlacesModel.objects.get(id=id)
    data = food.restaurants
    del data[int(jid-1)]

    food.save()
    messages.success(request, 'Restaurents or Food Deleted Successfully!')
    return redirect('destdetails', id)


def addrooms(request, id):
    login = request.session['login']
    place = PlacesModel.objects.get(id=id)

    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        location = request.POST['location']
        image = request.FILES['image']
       
        places_images_dir = os.path.join(
            settings.BASE_DIR, 'static', 'places_images')
      
        os.makedirs(places_images_dir, exist_ok=True)

      
        image_path = os.path.join('static/places_images/', image.name)
        print(image_path)
       
        with open(os.path.join(places_images_dir, image.name), 'wb') as img_file:
            for chunk in image.chunks():
                img_file.write(chunk)

        
        place.rooms.append(
            {'hotelname': name, 'location': location, 'desc': desc, 'img': image_path})

        place.save()

        messages.success(request, 'Rooms added successfully!')
        return redirect('addrooms', id)

    return render(request, 'addrooms.html', {'login': login, 'id': id})


def updaterooms(request, id, jid):
    login = request.session['login']
    place = PlacesModel.objects.get(id=id)
    data = place.rooms[int(jid-1)]
    print(data)
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        location = request.POST['location']
        if 'image' in request.FILES:
            print('==================')
            image = request.FILES['image']
            data['hotelname'] = name
            data['desc'] = desc
            data['location'] = location
           
            places_images_dir = os.path.join(
                settings.BASE_DIR, 'static', 'places_images')
           
            os.makedirs(places_images_dir, exist_ok=True)
          
            image_path = os.path.join(
                'static/places_images/', image.name)  # Path relative
     
            # n=random.randint(1111,9999)
            with open(os.path.join(places_images_dir, image.name), 'wb') as img_file:
                for chunk in image.chunks():
                    img_file.write(chunk)
            print(image_path)
            data['img'] = image_path
            # del data['image']
            place.save()
        else:
            data['hotelname'] = name
            data['desc'] = desc
            data['location'] = location
            place.save()

        messages.success(request, 'Room Updated Successfully!')
        return redirect('updaterooms', id, jid)

    return render(request, 'updaterooms.html', {'login': login, 'id': id, 'jid': jid, 'data': data})


def deleterooms(request, id, jid):
    login = request.session['login']
    room = PlacesModel.objects.get(id=id)
    data = room.rooms
    del data[int(jid-1)]

    room.save()
    messages.success(request, 'Room Deleted Successfully!')
    return redirect('destdetails', id)


def roomsingledest(request, id, jid):
    login = request.session['login']
    place = PlacesModel.objects.get(id=id)
    data = place.rooms[int(jid-1)]
    print(type(data))
    places = PlacesModel.objects.filter(id=id)
    return render(request, 'roomsingledest.html', {'login': login, 'data': data, 'places': places})


def foodsingledest(request, id, jid):
    login = request.session['login']
    place = PlacesModel.objects.get(id=id)
    data = place.restaurants[int(jid-1)]
    return render(request, 'foodsingledest.html', {'login': login, 'data': data})


def placesingledest(request, id, jid):
    login = request.session['login']
    place = PlacesModel.objects.get(id=id)

    data = place.places[int(jid-1)]
    # del data['']
    return render(request, 'placesingledest.html', {'login': login, 'data': data})


def destinations(request):
    login = request.session['login']
    dest = PlacesModel.objects.all()
    return render(request, 'destinations.html', {'login': login, 'data': dest})


def filter(request):
    login = request.session['login']
    if request.method == "POST":
        filter = request.POST['areatype']
        dest = PlacesModel.objects.filter(placetype__contains=filter)
    return render(request, 'destinations.html', {'login': login, 'data': dest})


def cart(request):
    login = request.session['login']
    email = request.session['email']
    cart = CartModel.objects.filter(email=email)

    return render(request, 'cart.html', {'login': login, 'cart': cart})


def addtocart(request):
    login = request.session['login']
    email = request.session['email']
    # data = json.loads(data)
    hotelname = request.GET['hotel']
    desc = request.GET['desc']
    location = request.GET['location']
    img = request.GET['image']

    cart = CartModel.objects.create(
        hotelname=hotelname,
        location=location,
        desc=desc,
        image=img,
        email=email

    )
    cart.save()
    return redirect('cart')


def removecart(request, id):
    login = request.session['login']
    email = request.session['email']
    cart = CartModel.objects.get(id=id)
    cart.delete()
    return redirect('cart')


def booknow(request, id):
    login = request.session['login']
    email = request.session['email']
    cart = CartModel.objects.get(id=id)
    book = BookingModel.objects.create(
        hotelname=cart.hotelname,
        location=cart.location,
        desc=cart.desc,
        image=cart.image,
        email=email

    )
    book.save()
    cart.delete()
    return redirect('bookings')


def bookings(request):
    login = request.session['login']
    email = request.session['email']
    bookings = BookingModel.objects.filter(email=email)
    return render(request, 'bookings.html', {'bookings': bookings, 'login': login})


def recommend(request):
    login = request.session['login']
    if request.method == 'POST':
 
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        health_conditions = request.POST.getlist('health_conditions')
        climate_preferences = request.POST.get('climate')
        activity_type = request.POST.getlist('activities')
        travel_budget = request.POST.get('budget')
        time_available = request.POST.get('time_available')
        current_location = request.POST.get('current_location')
        travel_companions = request.POST.get('companions')
        print(age, gender, health_conditions, climate_preferences, activity_type,
              travel_budget, time_available, current_location, travel_companions)

     
        file_path = r'dataset/unique_places_corrected_user_data.csv'
        df = pd.read_csv(file_path)

     
        place_details = {
            "Haridwar": {
                "description": "Haridwar, one of the holiest cities in India, lies in the state of Uttarakhand along the banks of the Ganges River. It is known for its spiritual atmosphere, sacred ghats, and the evening Ganga Aarti at Har Ki Pauri.",
                "activities": [
                    "Attend the mesmerizing Ganga Aarti at Har Ki Pauri during sunset.",
                    "Visit ancient temples like the Mansa Devi Temple and Chandi Devi Temple via a cable car.",
                    "Take a holy dip in the Ganges to cleanse yourself of sins.",
                    "Explore the Rajaji National Park for a glimpse of wildlife."
                ],
                "must_try_foods": [
                    "Aloo Puri at local street stalls.",
                    "Kachoris served with spicy chutney.",
                    "Lassi (a refreshing yogurt-based drink).",
                    "Chole Bhature from local eateries."
                ]
            },
            "Manali": {
                "description": "Manali, a picturesque hill station nestled in the Himalayas, is a haven for adventure enthusiasts and nature lovers alike. With its breathtaking views, lush valleys, and vibrant culture, it is the perfect getaway for thrill-seekers.",
                "activities": [
                    "Go paragliding in Solang Valley.",
                    "Trek to Hampta Pass or Bhrigu Lake for stunning mountain views.",
                    "Visit the Hidimba Devi Temple, an ancient shrine surrounded by towering deodar trees.",
                    "Enjoy river rafting in the Beas River.",
                    "Take a stroll along the lively Mall Road."
                ],
                "must_try_foods": [
                    "Siddu (steamed wheat buns filled with nuts and poppy seeds).",
                    "Trout Fish from local Himachali restaurants.",
                    "Momos with spicy dipping sauce.",
                    "Kullu Rajma (kidney beans cooked in Himachali spices)."
                ]
            },
            "Mumbai": {
                "description": "Mumbai, the financial capital of India, is a city that never sleeps. It is known for its bustling streets, colonial architecture, and the glitzy world of Bollywood. Mumbai’s diverse cultural heritage makes it a melting pot of people and experiences.",
                "activities": [
                    "Visit the iconic Gateway of India and take a ferry to Elephanta Caves.",
                    "Relax at Marine Drive or Juhu Beach.",
                    "Experience the vibrant nightlife in areas like Colaba and Bandra.",
                    "Explore the Chhatrapati Shivaji Maharaj Vastu Sangrahalaya (formerly Prince of Wales Museum).",
                    "Walk through the historic Crawford Market."
                ],
                "must_try_foods": [
                    "Vada Pav, a spicy potato fritter in a bun, Mumbai's favorite street food.",
                    "Pav Bhaji (buttery bread served with a mixed vegetable curry).",
                    "Bombay Sandwich, a toasted sandwich filled with spicy chutneys and vegetables.",
                    "Pani Puri from Chowpatty Beach."
                ]
            },
            "Tawang": {
                "description": "Tawang, located in Arunachal Pradesh, is renowned for its scenic beauty, spiritual ambiance, and its stunning monastery. Nestled in the mountains, Tawang offers peace, adventure, and breathtaking views of the Himalayas.",
                "activities": [
                    "Visit the majestic Tawang Monastery, the largest in India.",
                    "Take in the breathtaking views at Sela Pass, one of the highest motorable passes.",
                    "Pay respects at the Tawang War Memorial, dedicated to soldiers of the 1962 Sino-Indian war.",
                    "Explore the enchanting Nuranang Falls.",
                    "Trek in the beautiful Madhuri Lake area."
                ],
                "must_try_foods": [
                    "Thukpa (a hearty noodle soup with vegetables or meat).",
                    "Momos (steamed dumplings) served with a spicy chutney.",
                    "Zan, a local Monpa dish made from millet flour.",
                    "Butter Tea, traditional Tibetan tea."
                ]
            },
            "Jaisalmer": {
                "description": "Jaisalmer, known as the Golden City of Rajasthan, is famed for its yellow sandstone architecture, majestic forts, and the expansive Thar Desert. It’s a place where history comes alive through intricate havelis and centuries-",
                "activities": [
                    "Explore the magnificent Jaisalmer Fort, a living fort bustling with markets and old havelis.",
                    "Visit the Patwon Ki Haveli for a glimpse of Rajasthani craftsmanship.",
                    "Take a camel safari through the Thar Desert at sunset.",
                    "Spend a night in a desert camp under the starry sky.",
                    "Visit the haunting ruins of Kuldhara, an abandoned village."

                ],
                "must_try_foods": [
                    "Dal Baati Churma, a traditional Rajasthani dish of lentils, baked wheat balls, and sweetened crushed wheat..",
                    "Gatte Ki Sabzi (gram flour dumplings in spicy yogurt gravy).",
                    "Laal Maas, a spicy meat curry famous in Rajasthan",
                    "Makhaniya Lassi (sweetened yogurt drink) to beat the desert heat."
                ]
            },
            "Mahabaleshwar": {
                "description": "Mahabaleshwar, a scenic hill station in the Western Ghats of Maharashtra, is known for its lush greenery, numerous viewpoints, and strawberry farms. It’s a popular retreat for those looking to escape the city and relax amidst nature.",
                "activities": [

                    "Visit Arthur's Seat and other popular viewpoints like Elephant's Head Point for stunning views of valleys and the Sahyadri mountain range.",
                    "Enjoy boating at Venna Lake.",
                    "Visit the Mahabaleshwar Temple, an ancient temple dedicated to Lord Shiva.",
                    "Stroll through the Mapro Garden and taste fresh strawberry delights.",
                    "Trek to Pratapgad Fort, a historically significant site."
                ],
                "must_try_foods": [
                    "Fresh Strawberries with cream, a specialty of Mahabaleshwar.",
                    "Corn Patties, a local street food delight.",
                    "Puran Poli, a sweet flatbread filled with jaggery and lentils.",
                    "Strawberry Milkshake from Mapro Garden."
                ]
            },
            "Rameswaram": {
                "description": "Rameswaram, located in Tamil Nadu, is a significant pilgrimage site and part of the Char Dham Yatra. Known for its beautiful temples, pristine beaches, and historic connections to the Ramayana, Rameswaram is both spiritually enriching and picturesque.",
                "activities": [
                    "Visit the iconic Ramanathaswamy Temple, known for its long corridors and ornate carvings.",
                    "Walk across the Pamban Bridge for panoramic views of the sea.",
                    "Explore Dhanushkodi, the ghost town known for its history and stunning views.",
                    "Take a dip in the Agnitheertham, considered a sacred spot near the temple.",
                    "Relax at Ariyaman Beach, ideal for a peaceful evening."

                ],
                "must_try_foods": [
                    "Idli and Dosa served with traditional Tamil-style chutneys and sambar.",
                    "Chettinad Curry, known for its aromatic spices.",
                    "Pongal, a hearty dish made from rice and lentils.",
                    "Seafood, especially fresh prawns and fish curries."
                ]
            },
            "Puri": {
                "description": " Puri, located on the eastern coast in Odisha, is one of the four sacred Char Dham pilgrimage sites. It is best known for the Jagannath Temple and its vibrant Rath Yatra festival, as well as its golden beaches.",
                "activities": [
                    "Visit the famous Jagannath Temple, dedicated to Lord Jagannath, an incarnation of Lord Vishnu.",
                    "Witness the Rath Yatra if you visit during the festival season.",
                    "Spend a relaxing day at Puri Beach, enjoying the sun and sea.",
                    "Visit Chilika Lake, Asia's largest saltwater lagoon, known for birdwatching and boat rides.",
                    "Explore the Konark Sun Temple, a UNESCO World Heritage site nearby."

                ],
                "must_try_foods": [
                    "Khaja, a sweet pastry-like dessert offered as prasad at the Jagannath Temple.",
                    "Chhena Poda, a baked cottage cheese dessert.",
                    "Dalma, a traditional dish made with lentils and vegetables.",
                    "Pakhala Bhata, fermented rice served with accompaniments, a popular summer dish."
                ]
            },
            "Amritsar": {
                "description": " Amritsar, located in the state of Punjab, is a city known for its rich history, vibrant culture, and spiritual significance. The Golden Temple is the heart of the city, offering peace and a sense of belonging to visitors of all backgrounds.",
                "activities": [
                    "Visit the magnificent Golden Temple (Harmandir Sahib) and take part in the community kitchen (Langar).",
                    "Attend the Wagah Border Ceremony to witness the daily evening parade and ceremonial lowering of the flags.",
                    "Explore Jallianwala Bagh, a historic garden and memorial.",
                    "Shop at Hall Bazaar for traditional Punjabi clothes and handicrafts.",
                    "Walk through the bustling Guru Bazaar for traditional jewelry and souvenirs."

                ],
                "must_try_foods": [
                    "Amritsari Kulcha, stuffed bread served with spicy chickpeas.",
                    "Lassi, a sweet, frothy yogurt drink.",
                    "Makki di Roti and Sarson da Saag, a classic Punjabi winter dish.",
                    "Butter Chicken with naan, a quintessential taste of Punjab."
                ]
            },
            "Udaipur": {
                "description": "Udaipur, known as the 'City of Lakes,' is a gem in Rajasthan. It is famous for its beautiful lakes, grand palaces, and romantic ambiance, making it a popular destination for couples, history lovers, and anyone seeking an experience of royal grandeur.",
                "activities": [
                    "Take a boat ride on Lake Pichola and admire the beautiful Lake Palace.",
                    "Visit the grand City Palace, which offers stunning views of the lake and houses museums showcasing royal artifacts.",
                    "Explore the Saheliyon Ki Bari, a beautiful garden with fountains and marble pavilions.",
                    "Watch a traditional Rajasthani folk dance performance at Bagore Ki Haveli.",
                    "Enjoy a sunset view from the Monsoon Palace."
                ],
                "must_try_foods": [
                    "Dal Baati Churma, a signature Rajasthani dish made of lentils, wheat dumplings, and a sweet crumble.",
                    "Ghewar, a traditional sweet often enjoyed during festivals.",
                    "Laal Maas, a spicy mutton curry cooked with red chilies.",
                    "Kachori filled with spiced lentils, often served with tangy chutneys."
                ]
            },
            "Darjeeling": {
                "description": "Darjeeling, known as the 'Queen of the Hills,' is a beautiful town located in the foothills of the Himalayas. It’s famous for its sprawling tea estates, stunning views of Mount Kanchenjunga, and the iconic Darjeeling Himalayan Railway.",
                "activities": [
                    "Take a ride on the Darjeeling Himalayan Railway (Toy Train), a UNESCO World Heritage Site.",
                    "Visit the Tiger Hill at dawn for a spectacular sunrise over Mount Kanchenjunga.",
                    "Explore the lush Darjeeling Tea Gardens and learn about tea production.",
                    "Spend some peaceful time at the Ghoom Monastery.",
                    "Visit the Padmaja Naidu Himalayan Zoological Park, home to snow leopards and red pandas."
                ],
                "must_try_foods": [
                    "Darjeeling Tea, freshly brewed from the tea gardens.",
                    "Momos, Tibetan-style dumplings filled with meat or vegetables.",
                    "Thukpa, a traditional noodle soup, perfect for the cool weather.",
                    "Churpee, a local hard cheese made from yak milk."
                ]
            },
            "Shillong": {
                "description": "Shillong, often referred to as the 'Scotland of the East,' is the capital of Meghalaya. Known for its rolling hills, pleasant climate, and waterfalls, Shillong is the cultural and musical hub of the Northeast.",
                "activities": [
                    "Visit the breathtaking Elephant Falls and Sweet Falls.",
                    "Enjoy a boat ride on the serene Umiam Lake.",
                    "Explore the Don Bosco Centre for Indigenous Cultures, a museum showcasing the cultural heritage of the Northeast.",
                    "Take a stroll through the Laitlum Canyons for panoramic views of the valleys.",
                    "Shop at the Police Bazaar for local handicrafts and street food."
                ],
                "must_try_foods": [
                    "Jadoh, a Khasi rice dish cooked with meat, best enjoyed with local spices.",
                    "Tungrymbai, fermented soybeans cooked with pork and spices.",
                    "Momos, a popular street food filled with vegetables or meat.",
                    "Dohneiiong, a pork curry cooked with black sesame, rich in flavor."
                ]
            },
            "Pondicherry": {
                "description": "Pondicherry, now officially known as Puducherry, is a charming coastal town that reflects the legacy of French colonial rule in India. With its vibrant culture, serene beaches, and colonial architecture, it’s an ideal destination for a peaceful getaway.",
                "activities": [
                    "Stroll along the Promenade Beach and enjoy the beautiful views.",
                    "Explore the quaint French Quarter with its colorful colonial buildings and cafes.",
                    "Visit the Aurobindo Ashram, known for its tranquil atmosphere.",
                    "Spend time at Auroville, an experimental township dedicated to community and spiritual growth.",
                    "Enjoy water sports like kayaking and paddleboarding at Paradise Beach."
                ],
                "must_try_foods": [
                    "Croissants and other French-inspired baked goods from local cafes.",
                    "Seafood platters, including prawns, fish, and squid, cooked with local spices.",
                    "Creole Cuisine, a unique fusion of Tamil and French culinary traditions.",
                    "Filter Coffee, an authentic South Indian specialty found in many local cafes."
                ]
            },
            "Kerala": {
                "description": "Kerala, known as 'God's Own Country,' is located on the southwestern coast of India. It is famous for its backwaters, coconut-lined beaches, and lush green landscapes. The tranquil atmosphere makes it a favorite destination for nature lovers and those seeking relaxation.",
                "activities": [
                    "Take a houseboat cruise through the beautiful Alleppey backwaters.",
                    "Explore the Munnar Tea Gardens and enjoy breathtaking views of the hills.",
                    "Witness a traditional Kathakali dance performance.",
                    "Relax on the serene Varkala Beach or Kovalam Beach.",
                    "Visit the Periyar Wildlife Sanctuary for a boat safari and to see elephants in their natural habitat."
                ],
                "must_try_foods": [
                    "Appam with Stew, a fluffy rice pancake served with a creamy vegetable or meat stew.",
                    "Puttu and Kadala Curry, a breakfast favorite made of steamed rice cake and black chickpea curry.",
                    "Fish Moilee, a mild coconut-based fish curry.",
                    "Banana Chips, crispy and lightly salted, available at most street shops."
                ]
            },
            "Kodaikanal": {
                "description": "Kodaikanal, often referred to as the 'Princess of Hill Stations,' is a serene hill town in Tamil Nadu. With its misty mountains, beautiful lakes, and rolling green valleys, it offers a peaceful escape from city life.",
                "activities": [
                    "Take a boat ride on the scenic Kodaikanal Lake.",
                    "Visit the Coaker's Walk for breathtaking views of the valleys.",
                    "Trek to the Pillar Rocks to witness towering rock formations shrouded in mist.",
                    "Explore the Bryant Park, a botanical garden known for its collection of vibrant flowers.",
                    "Visit the Silver Cascade Falls, a stunning waterfall just outside of town."
                ],
                "must_try_foods": [
                    "Homemade Chocolates, available in local shops with a variety of flavors.",
                    "Bread Omelette, a common breakfast favorite at local eateries.",
                    "Plum Cake, a specialty baked treat often served during the winter months.",
                    "Hot Filter Coffee, a staple for visitors looking for warmth in the misty weather."
                ]
            },
            "Shimla": {
                "description": "Shimla, the capital of Himachal Pradesh, is one of India's most popular hill stations. It is known for its colonial charm, bustling Mall Road, and stunning views of the snow-capped Himalayas.",
                "activities": [
                    "Take a leisurely stroll along Mall Road and enjoy shopping for souvenirs.",
                    "Ride the Shimla-Kalka Toy Train, a UNESCO World Heritage site that offers spectacular views of the mountains.",
                    "Visit the historic Christ Church, one of the oldest churches in North India.",
                    "Explore the Viceregal Lodge, which was once the residence of the British Viceroy of India.",
                    "Hike to Jakhoo Temple to see the giant statue of Lord Hanuman."
                ],
                "must_try_foods": [
                    "Chana Madra, a traditional Himachali dish made with chickpeas in a yogurt-based gravy.",
                    "Sidu, a local bread served with ghee, often enjoyed during colder weather.",
                    "Aloo Palda, potatoes cooked in a yogurt-based curry.",
                    "Momos, steamed dumplings filled with vegetables or meat."
                ]
            },
            "Andaman": {
                "description": "The Andaman Islands are a tropical paradise known for their crystal-clear waters, white sandy beaches, and rich marine life. With a combination of adventure and relaxation, Andaman offers a unique island getaway.",
                "activities": [
                    "Go snorkeling or scuba diving at Havelock Island to explore vibrant coral reefs.",
                    "Relax at Radhanagar Beach, one of the most beautiful beaches in Asia.",
                    "Take a boat ride to Ross Island to explore historical British ruins.",
                    "Visit the Cellular Jail in Port Blair, which tells the story of India’s struggle for freedom.",
                    "Enjoy a glass-bottom boat ride to see the coral life without getting wet."
                ],
                "must_try_foods": [
                    "Grilled Fish, freshly caught and marinated with local spices.",
                    "Coconut Prawn Curry, a delicious curry made with prawns cooked in a coconut-based gravy.",
                    "Chili Crab, a spicy dish cooked with local flavors.",
                    "Fresh Coconut Water, a refreshing drink straight from the coconut, perfect for a hot day."
                ]
            },
            "Goa": {
                "description": "Goa, located on the western coast of India, is known for its stunning beaches, vibrant nightlife, and rich Portuguese heritage. It’s the perfect blend of relaxation, culture, and adventure, making it a favorite destination for domestic and international tourists alike.",
                "activities": [
                    "Relax on famous beaches like Baga, Calangute, and Anjuna.",
                    "Visit Basilica of Bom Jesus, a UNESCO World Heritage site.",
                    "Enjoy the Saturday Night Market at Arpora, famous for food, music, and handicrafts.",
                    "Take part in water sports like jet-skiing, parasailing, and banana boat rides.",
                    "Discover Goan culture by visiting Fontainhas, the Latin Quarter of Panaji."
                ],
                "must_try_foods": [
                    "Pork Vindaloo, a spicy and tangy Goan curry.",
                    "Goan Prawn Curry, prawns cooked in a coconut-based gravy with local spices.",
                    "Bebinca, a traditional Goan dessert made with layers of coconut and jaggery.",
                    "Feni, a local spirit made from cashew apples."
                ]
            },
            "Jaipur": {
                "description": "Jaipur, known as the 'Pink City,' is the capital of Rajasthan and is famous for its royal heritage, colorful bazaars, and beautiful architecture. It’s part of the Golden Triangle tourist circuit, offering visitors a rich cultural experience.",
                "activities": [
                    "Explore the magnificent Amber Fort and take an elephant ride to the top.",
                    "Visit the Hawa Mahal (Palace of Winds) and its stunning façade.",
                    "Discover the City Palace, an architectural marvel that is a blend of Rajasthani and Mughal styles.",
                    "Take a stroll through the Jantar Mantar, an astronomical observatory.",
                    "Shop for handicrafts, jewelry, and textiles at Johari Bazaar."
                ],
                "must_try_foods": [
                    "Dal Baati Churma, Rajasthan's signature dish made of lentils, baked wheat balls, and sweet crumble.",
                    "Laal Maas, a spicy mutton curry that packs a punch.",
                    "Ghewar, a sweet, honeycomb-like dessert made of flour and soaked in sugar syrup.",
                    "Kachori, a fried pastry filled with lentils or spicy potato, often served with tamarind chutney."
                ]
            },
            "Agra": {
                "description": "Agra, home to the iconic Taj Mahal, is a city in Uttar Pradesh that exudes romance, grandeur, and history. The city is part of the Golden Triangle and is renowned for its Mughal architecture, bustling markets, and rich culture.",
                "activities": [
                    "Visit the majestic Taj Mahal, one of the Seven Wonders of the World, at sunrise.",
                    "Explore the Agra Fort, a UNESCO World Heritage site with stunning red sandstone architecture.",
                    "Admire the exquisite Itmad-ud-Daulah's Tomb, also known as the Baby Taj.",
                    "Take a leisurely walk through Mehtab Bagh, offering stunning views of the Taj Mahal.",
                    "Shop for marble handicrafts, leather goods, and jewelry at Kinari Bazaar."
                ],
                "must_try_foods": [
                    "Petha, a soft, translucent sweet made from ash gourd, available in various flavors.",
                    "Bedai with Aloo Sabzi, a popular breakfast consisting of fried bread served with spicy potato curry.",
                    "Mughlai Cuisine, including kebabs, biryanis, and rich gravies inspired by Mughal cooking.",
                    "Dalmoth, a spicy lentil-based snack enjoyed by locals and tourists alike."
                ]
            },
            "Rishikesh": {
                "description": "Rishikesh, often called the 'Yoga Capital of the World,' is a peaceful town in Uttarakhand located on the banks of the Ganges River. Known for its spirituality, adventure sports, and scenic beauty, Rishikesh is a popular destination for those seeking both tranquility and thrills.",
                "activities": [
                    "Participate in a yoga retreat or attend meditation sessions at an ashram.",
                    "Experience river rafting on the Ganges, one of the most popular adventure activities in Rishikesh.",
                    "Visit the Lakshman Jhula and Ram Jhula, iconic suspension bridges over the Ganges.",
                    "Attend the evening Ganga Aarti at Triveni Ghat for a spiritual experience.",
                    "Trek to Neer Garh Waterfall and enjoy the serene beauty of the surrounding nature."
                ],
                "must_try_foods": [
                    "Aloo Puri, a favorite breakfast dish served at street-side stalls.",
                    "Chole Bhature, a spicy chickpea curry served with fluffy fried bread.",
                    "Ayurvedic Tea, infused with herbs and spices, available in many cafes.",
                    "Momos, a popular snack often served with spicy chutneys."
                ]
            },
            "Ahmedabad": {
                "description": "Ahmedabad, the largest city in Gujarat, is known for its vibrant culture, fascinating history, and thriving textile industry. The city is also recognized as India's first UNESCO World Heritage City due to its well-preserved architectural heritage.",
                "activities": [
                    "Visit the Sabarmati Ashram, the former home of Mahatma Gandhi, to learn about India's freedom struggle.",
                    "Explore the intricately carved Adalaj Stepwell, an architectural marvel.",
                    "Discover the magnificent Sidi Saiyyed Mosque, known for its stunning stone latticework.",
                    "Take a walk through Pols, traditional housing clusters unique to Ahmedabad.",
                    "Enjoy a leisurely evening at Kankaria Lake, which has a zoo, toy train, and food stalls."
                ],
                "must_try_foods": [
                    "Dhokla, a steamed savory cake made from fermented rice and chickpea batter.",
                    "Fafda and Jalebi, a classic combination of a fried savory snack with a sweet syrupy dessert.",
                    "Gujarati Thali, an elaborate meal consisting of various curries, breads, rice, and sweets.",
                    "Khakra, crispy, thin crackers enjoyed with pickles or chutney."
                ]
            },
            "Srinagar": {
                "description": "Srinagar, the summer capital of Jammu and Kashmir, is a paradise on Earth known for its stunning landscapes, tranquil lakes, and beautiful gardens. It’s famous for the serene Dal Lake with its shikaras (houseboats) and vibrant Mughal gardens.",
                "activities": [
                    "Take a shikara ride on Dal Lake or stay in one of the traditional houseboats.",
                    "Visit the Mughal Gardens, such as Shalimar Bagh and Nishat Bagh, known for their intricate design and stunning views.",
                    "Explore the ancient Shankaracharya Temple, located atop a hill overlooking the city.",
                    "Visit the Hazratbal Shrine, a revered site along the shores of Dal Lake.",
                    "Shop for pashmina shawls, saffron, and hand-carved wooden artifacts at the local markets."
                ],
                "must_try_foods": [
                    "Rogan Josh, a rich mutton curry with an aromatic blend of Kashmiri spices.",
                    "Kahwa, a traditional Kashmiri tea brewed with saffron, almonds, and spices.",
                    "Yakhni, a yogurt-based mutton curry cooked with delicate spices.",
                    "Modur Pulao, a sweet rice dish flavored with cinnamon, saffron, and dry fruits."
                ]
            },
            "Gangtok": {
                "description": "Gangtok, the capital of Sikkim, is a charming hill station that offers a mix of modernity and tradition, set against the backdrop of the Eastern Himalayas. It is famous for its monasteries, scenic views, and the majestic Kanchenjunga.",
                "activities": [
                    "Visit the Rumtek Monastery, one of Sikkim's largest and most significant monasteries.",
                    "Enjoy the stunning views of Mount Kanchenjunga from the Tashi Viewpoint.",
                    "Take a cable car ride to enjoy panoramic views of the city and the mountains.",
                    "Explore the MG Marg, a pedestrian-friendly street with plenty of shopping and dining options.",
                    "Visit the Namgyal Institute of Tibetology to learn about Tibetan culture and Buddhism."
                ],
                "must_try_foods": [
                    "Phagshapa, a pork dish cooked with radishes and chilies, popular in Sikkimese cuisine.",
                    "Gundruk Soup, a fermented leafy green vegetable soup.",
                    "Thenthuk, a Tibetan-style noodle soup that is hearty and comforting.",
                    "Chhurpi, a fermented cheese snack enjoyed by locals."
                ]
            },
            "Mysore": {
                "description": "Mysore, also known as Mysuru, is a city in Karnataka known for its rich cultural heritage, palaces, and silk. It’s particularly famous for the Mysore Palace and the grand Dasara Festival, attracting tourists from across the globe.",
                "activities": [
                    "Visit the stunning Mysore Palace, an architectural masterpiece with beautiful interiors.",
                    "Climb up to the Chamundi Hill to visit the Chamundeshwari Temple.",
                    "Explore the vibrant Devaraja Market for fruits, flowers, and traditional goods.",
                    "Spend a peaceful day at the Brindavan Gardens, famous for its musical fountain.",
                    "Learn about the history of Mysore at the Jaganmohan Palace and Art Gallery."
                ],
                "must_try_foods": [
                    "Mysore Pak, a rich and buttery dessert made with gram flour, sugar, and ghee.",
                    "Bisi Bele Bath, a spicy rice dish with lentils and vegetables.",
                    "Mysore Masala Dosa, a crispy dosa stuffed with spicy mashed potatoes.",
                    "Chiroti, a layered sweet pastry dusted with powdered sugar, often served with warm milk."
                ]
            },
            "Alleppey": {
                "description": "Alleppey, also known as Alappuzha, is often called the 'Venice of the East' due to its vast network of beautiful backwaters. It is famous for its tranquil houseboat cruises and lush green landscapes, making it one of Kerala's most popular tourist spots.",
                "activities": [
                    "Take a houseboat cruise through the serene backwaters and enjoy the natural beauty.",
                    "Visit Marari Beach, a less-crowded beach known for its clean sands and calm waters.",
                    "Explore Kumarakom Bird Sanctuary, a paradise for bird lovers.",
                    "Participate in the famous Nehru Trophy Snake Boat Race if visiting during August.",
                    "Walk through the Alleppey Lighthouse and learn about the maritime history of the region."
                ],
                "must_try_foods": [
                    "Karimeen Pollichathu, pearl spot fish marinated with spices and wrapped in banana leaves.",
                    "Appam with Stew, a soft, fluffy rice pancake served with a mild vegetable or chicken stew.",
                    "Puttu and Kadala Curry, a steamed rice cake served with spicy black chickpea curry.",
                    "Tapioca and Fish Curry, a traditional dish popular in Alleppey’s backwater regions."
                ]
            },
            "Hampi": {
                "description": "Hampi, a UNESCO World Heritage site in Karnataka, is an ancient city full of ruins from the Vijayanagara Empire. It’s known for its unique boulder-strewn landscape, ancient temples, and architectural marvels that speak of a bygone era.",
                "activities": [
                    "Explore the magnificent Virupaksha Temple, dedicated to Lord Shiva.",
                    "Take a coracle ride across the Tungabhadra River.",
                    "Visit the Vijaya Vittala Temple, known for its iconic Stone Chariot and musical pillars.",
                    "Climb up to Matanga Hill for a beautiful sunrise or sunset over the ruins.",
                    "Wander through the Royal Enclosure and discover ancient palaces and bathing areas."
                ],
                "must_try_foods": [
                    "Bisi Bele Bath, a spicy rice and lentil dish that’s popular throughout Karnataka.",
                    "Puliyogare, a tangy rice dish made with tamarind and peanuts.",
                    "Ragi Mudde, steamed finger millet balls served with sambar or chutney.",
                    "Jolada Roti, a traditional flatbread made from sorghum, often served with various curries."
                ]
            },
            "Kolkata": {
                "description": "Kolkata, the capital of West Bengal, is often referred to as the 'City of Joy.' It is known for its colonial-era architecture, vibrant culture, literary heritage, and artistic spirit. Kolkata is also famous for its iconic Howrah Bridge and bustling streets.",
                "activities": [
                    "Visit the majestic Victoria Memorial, an iconic landmark built in memory of Queen Victoria.",
                    "Take a leisurely boat ride on the Hooghly River and enjoy the views of the Howrah Bridge.",
                    "Explore the Indian Museum, the oldest and largest museum in India, with a vast collection of artifacts.",
                    "Visit the iconic Dakshineswar Kali Temple and Belur Math, both known for their spiritual significance.",
                    "Enjoy a tram ride, one of the last cities in the world to have running tram services."
                ],
                "must_try_foods": [
                    "Kolkata Biryani, a flavorful rice dish that’s known for its subtle flavors and the addition of potatoes.",
                    "Kathi Rolls, flatbreads rolled up with a variety of fillings like chicken, paneer, and vegetables.",
                    "Rasgulla, a spongy, syrupy dessert made from chhena and semolina.",
                    "Puchka (Pani Puri), crispy puris filled with tangy tamarind water, a favorite street snack."
                ]
            },
            "Khajuraho": {
                "description": "Khajuraho, located in Madhya Pradesh, is famous for its magnificent group of Hindu and Jain temples known for their intricate erotic carvings. This UNESCO World Heritage site reflects the rich artistic heritage of India and is a window into medieval temple architecture.",
                "activities": [
                    "Visit the Khajuraho Group of Temples, renowned for their beautiful and intricately carved sculptures depicting various aspects of life.",
                    "Explore the Western Group of Temples, which is the most popular cluster for tourists.",
                    "Watch the light and sound show at the temples in the evening for an immersive experience.",
                    "Take part in a yoga session at one of the temple grounds to connect with the spiritual ambiance.",
                    "Visit the Archaeological Museum to learn about the history of the temples and the Chandela dynasty."
                ],
                "must_try_foods": [
                    "Bhutte Ki Kees, a traditional dish made of grated corn cooked with spices.",
                    "Sabudana Khichdi, a light dish made with sago pearls, potatoes, and peanuts, popular in Madhya Pradesh.",
                    "Poha, a light breakfast made from flattened rice with spices and vegetables.",
                    "Jalebi, a crispy, syrup-soaked dessert that is enjoyed by locals and tourists alike."
                ]
            },
            "Bhopal": {
                "description": "Bhopal, the capital of Madhya Pradesh, is known as the 'City of Lakes' due to its numerous natural and artificial lakes. The city has a unique blend of old-world charm and modernity, with historical landmarks, bustling bazaars, and serene parks.",
                "activities": [
                    "Visit the Taj-ul-Masajid, one of the largest mosques in India.",
                    "Take a boat ride on the Upper Lake (Bhojtal) to enjoy the peaceful waters and the beautiful sunset.",
                    "Explore the Bhimbetka Rock Shelters, a UNESCO World Heritage site with prehistoric cave paintings.",
                    "Walk through Van Vihar National Park and observe the rich flora and fauna.",
                    "Visit the State Museum to see the sculptures, artifacts, and exhibits showcasing the cultural heritage of Madhya Pradesh."
                ],
                "must_try_foods": [
                    "Bhopali Gosht Korma, a flavorful mutton curry with a mix of traditional spices.",
                    "Poha Jalebi, a classic breakfast combination enjoyed by the locals.",
                    "Shami Kebabs, minced meat patties mixed with aromatic spices.",
                    "Bafla, wheat dumplings typically served with dal and ghee."
                ]
            },
            "Pachmarhi": {
                "description": "Pachmarhi, known as the 'Queen of Satpura,' is a serene hill station in Madhya Pradesh. It is known for its verdant landscape, cascading waterfalls, and colonial charm. It’s a UNESCO Biosphere Reserve and a perfect retreat for nature lovers and trekkers.",
                "activities": [
                    "Visit the Bee Falls, a popular spot known for its refreshing water and scenic surroundings.",
                    "Explore the Jata Shankar Caves, natural caves with intriguing rock formations and a small shrine.",
                    "Take in the panoramic views from Dhoopgarh, the highest point in the Satpura Range, best visited during sunset.",
                    "Visit the Pandav Caves, believed to have been used by the Pandavas during their exile.",
                    "Go on a jungle safari in the Satpura Tiger Reserve to explore the rich wildlife."
                ],
                "must_try_foods": [
                    "Bhutte Ka Kees, a dish made of grated corn cooked with milk and spices.",
                    "Dal Bafla, wheat dumplings served with dal, often accompanied by ghee and chutney.",
                    "Makai Poha, a unique version of poha made with corn, available in local eateries.",
                    "Aloo Bharta, mashed potatoes seasoned with spices, often enjoyed with roti."
                ]
            },
            "Majuli": {
                "description": "Majuli, located in Assam, is the largest river island in the world and is known for its unique cultural heritage and natural beauty. Surrounded by the Brahmaputra River, Majuli is an important center for Vaishnavism and is famous for its serene landscape, tribal culture, and monasteries.",
                "activities": [
                    "Visit the Satras (Vaishnavite monasteries) such as Kamalabari Satra and Auniati Satra to learn about the culture and history.",
                    "Take a ferry ride across the Brahmaputra River and enjoy the scenic views.",
                    "Experience the Raas Leela Festival, a cultural celebration with music, dance, and performances.",
                    "Interact with the Mishing tribe and learn about their traditional way of life.",
                    "Explore the island’s vibrant handicrafts and pottery made by the local artisans."
                ],
                "must_try_foods": [
                    "Pitha, a traditional Assamese rice cake made during festivals.",
                    "Masor Tenga, a tangy fish curry made with tomatoes and lemon, popular in Assamese cuisine.",
                    "Tenga Dal, a sour lentil soup, often served with steamed rice.",
                    "Apong, a traditional rice beer made by the Mishing tribe."
                ]
            },
            "Ranchi": {
                "description": "Ranchi, the capital of Jharkhand, is known for its beautiful waterfalls, rich tribal culture, and natural beauty. It is often called the 'City of Waterfalls' and serves as a gateway to explore the tribal heartland of India.",
                "activities": [
                    "Visit the stunning Dassam Falls and Hundru Falls, popular for their scenic beauty.",
                    "Take in the panoramic views from Tagore Hill, named after the famous poet Rabindranath Tagore.",
                    "Visit the Ranchi Lake and take a boat ride to enjoy the peaceful surroundings.",
                    "Explore the Rock Garden, which offers beautiful views of Kanke Dam.",
                    "Visit the Pahari Mandir, dedicated to Lord Shiva, located atop a hill with a view of the city."
                ],
                "must_try_foods": [
                    "Litti Chokha, a dish made of wheat flour balls filled with gram flour and served with mashed spiced vegetables.",
                    "Thekua, a traditional sweet made with wheat flour, sugar, and dry fruits.",
                    "Chilka Roti, a type of savory pancake made from rice flour and spices.",
                    "Handia, a local rice beer made during festivals and tribal celebrations."
                ]
            },
            "Gulmarg": {
                "description": "Gulmarg, located in Jammu and Kashmir, is a famous hill station known for its snow-capped mountains, ski slopes, and scenic beauty. It’s an ideal destination for adventure seekers and nature lovers, with activities ranging from skiing to gondola rides.",
                "activities": [
                    "Take a ride on the Gulmarg Gondola, one of the highest cable cars in the world, offering breathtaking views.",
                    "Go skiing or snowboarding in the winter, as Gulmarg is one of India’s top ski destinations.",
                    "Visit the beautiful Alpather Lake, located at the base of the Apharwat peak.",
                    "Play a round of golf at the Gulmarg Golf Course, one of the highest golf courses in the world.",
                    "Enjoy a peaceful walk through the meadows of Gulmarg during the summer, surrounded by wildflowers."
                ],
                "must_try_foods": [
                    "Rogan Josh, a flavorful lamb dish cooked with Kashmiri spices.",
                    "Yakhni, a yogurt-based mutton curry that’s mild yet aromatic.",
                    "Kahwa, a traditional Kashmiri tea infused with saffron and almonds.",
                    "Tabak Maaz, lamb ribs simmered in spices and then fried until crispy."
                ]
            },
            "Varanasi": {
                "description": "Varanasi, one of the world's oldest continually inhabited cities, is located on the banks of the Ganges in Uttar Pradesh. Known for its ghats, temples, and spiritual aura, Varanasi is a sacred city for Hindus and a major cultural hub.",
                "activities": [
                    "Attend the mesmerizing Ganga Aarti at Dashashwamedh Ghat during the evening.",
                    "Take an early morning boat ride on the Ganges to witness the beautiful sunrise and rituals along the ghats.",
                    "Visit the ancient Kashi Vishwanath Temple, dedicated to Lord Shiva.",
                    "Explore the narrow lanes of Old Varanasi and shop for silk sarees, handicrafts, and souvenirs.",
                    "Visit Sarnath, where Gautama Buddha delivered his first sermon after enlightenment."
                ],
                "must_try_foods": [
                    "Kachori Sabzi, a popular breakfast dish consisting of fried bread stuffed with lentils and served with spicy vegetable curry.",
                    "Banarasi Paan, a betel leaf preparation that’s famous throughout India.",
                    "Lassi, served in a kulhad (clay pot), rich and refreshing.",
                    "Tamatar Chaat, a spicy, tangy snack made with tomatoes, potatoes, and a variety of spices."
                ]
            },
            "Chandigarh": {
                "description": "Chandigarh, known as 'The City Beautiful,' is the capital of both Punjab and Haryana. Designed by the Swiss-French architect Le Corbusier, Chandigarh is known for its well-planned layout, green spaces, and modern architecture.",
                "activities": [
                    "Visit the Rock Garden, a unique garden created entirely from industrial and home waste.",
                    "Take a boat ride on Sukhna Lake, a beautiful man-made reservoir in the heart of the city.",
                    "Explore the beautiful Rose Garden, home to thousands of varieties of roses and other flowers.",
                    "Admire the architecture of the Capitol Complex, a UNESCO World Heritage site.",
                    "Shop at Sector 17 Market, known for its variety of shops and bustling atmosphere."
                ],
                "must_try_foods": [
                    "Chole Bhature, spicy chickpeas served with fried bread, a favorite dish in Punjab.",
                    "Amritsari Kulcha, a stuffed flatbread typically served with butter and pickle.",
                    "Lassi, a thick yogurt-based drink, often topped with cream or nuts.",
                    "Tandoori Chicken, chicken marinated in spices and cooked in a clay oven, served with mint chutney."
                ]
            },
            "Dwarka": {
                "description": "Dwarka, located in the state of Gujarat, is one of the seven oldest religious cities in India and is part of the Char Dham pilgrimage circuit. It is known for its ancient temples and beautiful coastal views.",
                "activities": [
                    "Visit the famous Dwarkadhish Temple, dedicated to Lord Krishna, and known for its intricate carvings.",
                    "Take a boat ride to Bet Dwarka Island, believed to be the residence of Lord Krishna.",
                    "Explore the Rukmini Devi Temple, dedicated to Lord Krishna's consort.",
                    "Witness the evening aarti at Dwarkadhish Temple for a spiritual experience.",
                    "Walk along Gomti Ghat and visit the nearby temples."
                ],
                "must_try_foods": [
                    "Gujarati Thali, a traditional platter consisting of various curries, breads, rice, and sweets.",
                    "Thepla, a flatbread made with whole wheat flour and fenugreek leaves.",
                    "Khandvi, a savory snack made with gram flour, rolled and garnished with mustard seeds and grated coconut.",
                    "Shrikhand, a sweet yogurt-based dessert flavored with saffron and cardamom."
                ]
            },
            "Chikmagalur": {
                "description": "Chikmagalur, a charming hill station in Karnataka, is known for its lush coffee plantations, misty hills, and beautiful trekking trails. It is a perfect destination for nature lovers and those seeking a peaceful retreat.",
                "activities": [
                    "Visit the Mullayanagiri Peak, the highest peak in Karnataka, for breathtaking views.",
                    "Take a tour of coffee plantations and learn about coffee production.",
                    "Trek to Baba Budangiri, a mountain range known for its scenic views and caves.",
                    "Visit the Hebbe Falls, a stunning waterfall that requires an adventurous ride and trek to reach.",
                    "Explore the ancient Hirekolale Lake during sunset."
                ],
                "must_try_foods": [
                    "Kotte Kadubu, a type of idli steamed in jackfruit leaves, giving it a unique flavor.",
                    "Akki Roti, a flatbread made from rice flour, served with chutney.",
                    "Coffee, freshly brewed from locally grown beans.",
                    "Neer Dosa, a soft, lacy dosa made from rice batter, served with chutney or curry."
                ]
            },
            "Lakshadweep": {
                "description": "Lakshadweep, an archipelago in the Arabian Sea, is known for its turquoise waters, pristine beaches, and vibrant marine life. It is a tropical paradise ideal for those looking to explore untouched beauty and underwater wonders.",
                "activities": [
                    "Go snorkeling or scuba diving in the crystal-clear waters to explore coral reefs.",
                    "Relax on the pristine beaches of Agatti Island or Bangaram Island.",
                    "Take a glass-bottom boat ride to see the colorful marine life without getting wet.",
                    "Explore Kavaratti Island, known for its beautiful lagoons and scenic views.",
                    "Visit the Marine Aquarium to learn about the diverse marine species found in the region."
                ],
                "must_try_foods": [
                    "Tuna Fish Curry, a spicy fish curry cooked with coconut and local spices.",
                    "Coconut Rice, a fragrant rice dish made with grated coconut.",
                    "Fried Fish, freshly caught and fried with local spices.",
                    "Parotta, a layered flatbread served with various curries."
                ]
            },
            "Jodhpur": {
                "description": "Jodhpur, known as the 'Blue City' due to its blue-painted houses, is a vibrant city in Rajasthan. It is famous for its grand palaces, majestic forts, and rich cultural heritage.",
                "activities": [
                    "Visit the imposing Mehrangarh Fort, one of the largest forts in India, with panoramic views of the blue city.",
                    "Explore the Umaid Bhawan Palace, part of which is a luxury hotel, and part is a museum.",
                    "Stroll through the Rao Jodha Desert Rock Park, which showcases the unique flora of the Thar Desert.",
                    "Shop for handicrafts, jewelry, and spices at the bustling Clock Tower Market.",
                    "Visit the Jaswant Thada, a beautiful marble cenotaph built in memory of Maharaja Jaswant Singh."
                ],
                "must_try_foods": [
                    "Dal Baati Churma, a signature Rajasthani dish made with lentils, wheat dumplings, and sweet crumble.",
                    "Mirchi Vada, a spicy snack made with green chilies stuffed with potatoes and deep-fried.",
                    "Makhaniya Lassi, a sweet, thick yogurt drink, perfect for cooling down in the desert heat.",
                    "Gatte Ki Sabzi, gram flour dumplings cooked in a spicy yogurt-based curry."
                ]
            },
            "Mount Abu": {
                "description": "Mount Abu, the only hill station in Rajasthan, is a popular destination known for its cool climate, scenic beauty, and beautiful Jain temples. Nestled in the Aravalli Range, it is a refreshing retreat from the desert heat.",
                "activities": [
                    "Visit the Dilwara Temples, renowned for their exquisite marble carvings and intricate designs.",
                    "Take a boat ride on Nakki Lake and enjoy the serene atmosphere.",
                    "Enjoy panoramic views from Sunset Point, a popular spot for tourists.",
                    "Visit the Guru Shikhar, the highest point in the Aravalli Range, for breathtaking views.",
                    "Explore the Mount Abu Wildlife Sanctuary, home to a variety of flora and fauna."
                ],
                "must_try_foods": [
                    "Rajasthani Thali, a platter that includes dishes like dal, baati, churma, gatte ki sabzi, and more.",
                    "Rabri, a sweet, condensed milk-based dessert flavored with saffron and cardamom.",
                    "Kachori, a fried pastry filled with spiced lentils, often enjoyed as a snack.",
                    "Pani Puri, a popular street food, crispy puris filled with spicy tamarind water."
                ]
            },
            "Lonavala": {
                "description": "Lonavala, a hill station in Maharashtra, is known for its scenic beauty, waterfalls, and lush greenery. It is a popular getaway from Mumbai and Pune, offering a peaceful retreat in the Western Ghats.",
                "activities": [
                    "Visit the famous Bhushi Dam, a popular picnic spot, especially during the monsoon season.",
                    "Explore the Karla Caves and Bhaja Caves, ancient rock-cut Buddhist shrines.",
                    "Trek to Lohagad Fort or Rajmachi Fort for panoramic views of the surrounding hills.",
                    "Enjoy the beautiful Lonavala Lake, surrounded by greenery.",
                    "Shop for chikki, a traditional sweet made from jaggery and nuts."
                ],
                "must_try_foods": [
                    "Chikki, a crunchy sweet made from jaggery and peanuts or other nuts, a specialty of Lonavala.",
                    "Vada Pav, a popular street snack in Maharashtra, made of a spicy potato patty served in a bun.",
                    "Misal Pav, a spicy curry made of sprouts served with bread, garnished with onions, lemon, and sev.",
                    "Bhajiyas, crispy fried fritters, perfect for enjoying with hot tea during the monsoon."
                ]
            },
            "Tirupati": {
                "description": "Tirupati, located in Andhra Pradesh, is one of the most visited pilgrimage destinations in India. It is famous for the Sri Venkateswara Temple, located on the Tirumala hills, which draws millions of devotees each year.",
                "activities": [
                    "Visit the Sri Venkateswara Temple, dedicated to Lord Venkateswara, and take part in the various rituals.",
                    "Explore the Kapila Theertham, a beautiful waterfall located at the base of the Tirumala hills.",
                    "Visit the Sri Kalahasti Temple, known for its intricate carvings and significance in Hindu mythology.",
                    "Trek to Talakona Waterfalls, the highest waterfall in Andhra Pradesh.",
                    "Enjoy the spiritual ambiance of the ISKCON Temple in Tirupati."
                ],
                "must_try_foods": [
                    "Laddu Prasadam, a sweet offered as prasad at the Tirumala temple, famous throughout India.",
                    "Pulihora, a tangy tamarind rice dish, commonly offered in temples.",
                    "Dosas, crispy rice pancakes served with coconut chutney and sambar.",
                    "Pongal, a savory dish made with rice and lentils, often enjoyed for breakfast."
                ]
            },
            "Nainital": {
                "description": "Nainital, a charming hill station in Uttarakhand, is known for its beautiful lakes, scenic views, and pleasant climate. Surrounded by lush hills, it is a popular destination for families and couples.",
                "activities": [
                    "Take a boat ride on the picturesque Naini Lake and enjoy the surrounding hills.",
                    "Visit the Naina Devi Temple, located on the banks of Naini Lake.",
                    "Ride the cable car to Snow View Point for a panoramic view of the Himalayas.",
                    "Stroll along the Mall Road, lined with shops, eateries, and beautiful lake views.",
                    "Trek to Tiffin Top for a picnic and stunning views of the surrounding landscape."
                ],
                "must_try_foods": [
                    "Aloo ke Gutke, a local dish made from boiled potatoes seasoned with local spices.",
                    "Bhatt ki Churkani, a black bean curry that is a Kumaoni specialty.",
                    "Ras, a curry made from lentils, typically served with steamed rice.",
                    "Bal Mithai, a sweet made from khoya and coated with sugar balls."
                ]
            },
            "Mussoorie": {
                "description": "Mussoorie, also known as the 'Queen of the Hills,' is a picturesque hill station in Uttarakhand. It is known for its scenic beauty, colonial heritage, and cool climate, making it a popular getaway for tourists.",
                "activities": [
                    "Take a walk along the Camel's Back Road, offering beautiful views of the mountains.",
                    "Visit the Kempty Falls, a popular picnic spot with a cascading waterfall.",
                    "Ride the cable car to Gun Hill, the second-highest peak in Mussoorie, for panoramic views.",
                    "Explore the Mussoorie Mall Road for shopping, dining, and entertainment.",
                    "Visit Lal Tibba, the highest point in Mussoorie, for stunning views of the snow-capped Himalayas."
                ],
                "must_try_foods": [
                    "Aloo ke Gutke, a local potato dish cooked with spices, enjoyed by the residents of Uttarakhand.",
                    "Chole Bhature, a popular North Indian dish served in most eateries in Mussoorie.",
                    "Pahadi Chicken, a traditional spicy chicken curry, often enjoyed with steamed rice.",
                    "Momos, steamed dumplings that are a favorite snack among tourists."
                ]
            },
            "Sundarbans": {
                "description": "The Sundarbans, located in West Bengal, is the largest mangrove forest in the world and a UNESCO World Heritage site. Known for its unique ecosystem, it is home to the famous Royal Bengal Tiger, diverse wildlife, and a network of tidal waterways and islands.",
                "activities": [
                    "Take a boat safari through the mangrove waterways to spot wildlife, including the elusive Royal Bengal Tiger.",
                    "Visit the Sajnekhali Bird Sanctuary to see various species of birds such as kingfishers, herons, and eagles.",
                    "Explore Dobanki Watch Tower for a panoramic view of the forest and observe wildlife from a safe elevation.",
                    "Spend time at Sudhanyakhali Watch Tower, a great place to spot deer, crocodiles, and tigers.",
                    "Interact with the local communities and learn about their unique lifestyle in harmony with the forest."
                ],
                "must_try_foods": [
                    "Bhapa Ilish, steamed hilsa fish cooked with mustard paste, a traditional Bengali delicacy.",
                    "Chingri Malai Curry, prawns cooked in a creamy coconut milk gravy, popular throughout Bengal.",
                    "Panta Bhat, fermented rice served with fried fish and vegetables, often enjoyed during festivals.",
                    "Mocha Ghonto, a traditional dish made from banana flowers, seasoned with Bengali spices."
                ]
            },
            "Kumarakom": {
                "description": "Kumarakom, located in Kerala, is a small village known for its picturesque backwaters, bird sanctuary, and serene landscape. It’s a perfect destination for those looking to relax and experience the natural beauty of Kerala’s waterways.",
                "activities": [
                    "Take a houseboat cruise through the backwaters of Vembanad Lake and enjoy the tranquil environment.",
                    "Visit the Kumarakom Bird Sanctuary, a paradise for bird watchers, where you can spot migratory birds.",
                    "Experience a traditional Ayurvedic massage, offered by local wellness centers.",
                    "Visit the Pathiramanal Island, a small scenic island in Vembanad Lake, accessible by boat.",
                    "Enjoy a canoe ride through the narrow canals to explore village life and the lush landscape."
                ],
                "must_try_foods": [
                    "Karimeen Pollichathu, pearl spot fish marinated with spices, wrapped in banana leaves, and grilled.",
                    "Fish Moilee, a mild coconut-based fish curry, a signature dish in Kerala.",
                    "Appam and Stew, a soft, fluffy rice pancake served with a rich, mildly spiced vegetable or chicken stew.",
                    "Kappa and Meen Curry, boiled tapioca served with spicy fish curry."
                ]
            },
            "Aizawl": {
                "description": "Aizawl, the capital of Mizoram, is a picturesque hill city known for its vibrant culture, scenic landscapes, and cool climate. It offers a peaceful escape from the hustle and bustle of city life, surrounded by lush hills and traditional tribal villages.",
                "activities": [
                    "Visit the Solomon’s Temple, an iconic structure that is a major religious site in Mizoram.",
                    "Explore the Durtlang Hills for breathtaking views of the city and the surrounding landscape.",
                    "Spend time at the State Museum, which showcases Mizo history, culture, and traditions.",
                    "Visit the Reiek Tlang village to experience Mizo culture and enjoy panoramic views of the surrounding hills.",
                    "Explore the bustling Bara Bazaar, a local market offering traditional handicrafts and regional delicacies."
                ],
                "must_try_foods": [
                    "Bai, a popular dish made from boiled vegetables, sometimes mixed with pork or bamboo shoots.",
                    "Vawksa Rep, smoked pork cooked with bamboo shoots and herbs, a staple in Mizo cuisine.",
                    "Arsa Buhchiar, a traditional chicken rice dish, often served during special occasions.",
                    "Zu Tea, a local black tea, often enjoyed in the morning or evening."
                ]
            },
            "Bhubaneswar": {
                "description": "Bhubaneswar, the capital of Odisha, is known as the 'City of Temples' due to its rich history and impressive collection of ancient temples. It is a perfect destination for history enthusiasts, offering a glimpse into India's glorious past through its architecture.",
                "activities": [
                    "Visit the iconic Lingaraj Temple, one of the oldest and most revered temples in Bhubaneswar.",
                    "Explore the Udayagiri and Khandagiri Caves, ancient rock-cut caves with inscriptions and carvings.",
                    "Discover the intricate architecture of the Mukteswara Temple, known as the 'Gem of Odisha'.",
                    "Take a stroll around the Bindu Sagar Lake, a sacred lake surrounded by temples.",
                    "Visit the Nandankanan Zoological Park, a popular zoo that also has a botanical garden and safari."
                ],
                "must_try_foods": [
                    "Chhena Poda, a traditional dessert made of baked cottage cheese with caramelized sugar.",
                    "Pakhala Bhata, fermented rice served with fried vegetables and badi chura, typically enjoyed during the summer.",
                    "Dalma, a lentil-based dish cooked with vegetables, a staple in Odia cuisine.",
                    "Rasagola, a spongy sweet made from chhena, originated in Odisha and is enjoyed all over the state."
                ]
            },
            "Daman": {
                "description": "Daman, located on the western coast of India, is part of the Union Territory of Daman and Diu. It is known for its scenic beaches, colonial architecture, and relaxed atmosphere, making it a popular getaway destination for travelers seeking a coastal retreat.",
                "activities": [
                    "Relax on Jampore Beach, known for its calm waters and scenic views.",
                    "Visit the Moti Daman Fort, which showcases Portuguese colonial architecture and offers a glimpse into Daman's history.",
                    "Explore the Bom Jesus Church, a beautiful old church built during Portuguese rule.",
                    "Take a walk through the Daman Lighthouse and enjoy panoramic views of the Arabian Sea.",
                    "Visit the Devka Beach, a rocky beach with amusement parks and local eateries."
                ],
                "must_try_foods": [
                    "Seafood Platter, including freshly caught fish, prawns, and crabs cooked in a variety of styles.",
                    "Chicken Bullet, a spicy chicken preparation popular among locals.",
                    "Portuguese Wine, reflecting the Portuguese influence on Daman's culture.",
                    "Prawn Curry, a local delicacy cooked with coconut and spices, best enjoyed with rice."
                ]
            },
            "Nagaland": {
                "description": "Nagaland, located in the northeastern part of India, is a land of festivals, rich tribal culture, and scenic landscapes. Known for its vibrant heritage, Nagaland is home to various tribes, each with its unique traditions, attire, and customs.",
                "activities": [
                    "Attend the famous Hornbill Festival held annually in December, showcasing the rich culture, dance, and music of the Naga tribes.",
                    "Visit the Kohima War Cemetery, a memorial dedicated to the soldiers who fought in World War II.",
                    "Explore the traditional Naga Villages like Khonoma, which offer insights into the local culture and sustainable living practices.",
                    "Trek to Dzukou Valley, known for its breathtaking views, lush green hills, and seasonal flowers.",
                    "Discover Kisama Heritage Village, the site of the Hornbill Festival, and learn about the Naga way of life."
                ],
                "must_try_foods": [
                    "Smoked Pork with Bamboo Shoots, a traditional Naga dish flavored with bamboo and spices.",
                    "Axone (Fermented Soybean), used in various dishes to add a unique flavor.",
                    "Anishi, a fermented yam leaf dish commonly cooked with meat.",
                    "Galho, a Naga version of khichdi, made with rice, vegetables, and meat."
                ]
            },
            "Cherrapunji": {
                "description": "Cherrapunji, also known as Sohra, is a town in Meghalaya that is famous for its record-breaking rainfall and lush green landscapes. It is home to many beautiful waterfalls, root bridges, and one of the wettest places on Earth.",
                "activities": [
                    "Visit the famous Nohkalikai Falls, the tallest plunge waterfall in India, offering breathtaking views.",
                    "Trek to the Double Decker Living Root Bridge in Nongriat, a natural marvel formed from the roots of rubber trees.",
                    "Explore the Mawsmai Caves, a network of limestone caves with beautiful stalactites and stalagmites.",
                    "Spend time at Seven Sisters Waterfalls, which offers a stunning view during the monsoon.",
                    "Visit the Eco Park, which provides panoramic views of the surrounding valleys and waterfalls."
                ],
                "must_try_foods": [
                    "Jadoh, a Khasi dish made with rice and meat, seasoned with turmeric and spices.",
                    "Dohneiiong, a pork dish cooked with black sesame seeds.",
                    "Tungrymbai, fermented soybeans cooked with pork and herbs.",
                    "Pumaloi, a type of steamed rice cake, usually enjoyed with vegetables or meat."
                ]
            },
            "Bikaner": {
                "description": "Bikaner, located in the heart of Rajasthan, is known for its majestic forts, vibrant culture, and delicious snacks. The city's architecture, bustling markets, and golden sand dunes give it a unique charm and make it a popular tourist destination.",
                "activities": [
                    "Visit the Junagarh Fort, a magnificent structure with beautiful palaces, courtyards, and balconies.",
                    "Explore the Karni Mata Temple in Deshnoke, also known as the Rat Temple, due to the thousands of rats considered sacred.",
                    "Take a camel safari in the Thar Desert and enjoy the unique landscape of sand dunes.",
                    "Visit the Lalgarh Palace, known for its beautiful architecture and lush gardens.",
                    "Enjoy the Bikaner Camel Festival, held annually, which showcases camel races, dances, and performances."
                ],
                "must_try_foods": [
                    "Bikaneri Bhujia, a spicy fried snack made from gram flour and spices, famous across India.",
                    "Rajasthani Gatta Curry, gram flour dumplings cooked in a tangy yogurt-based gravy.",
                    "Ker Sangri, a traditional desert dish made with dried berries and beans.",
                    "Rabri, a thickened, sweetened milk dish, flavored with cardamom and garnished with nuts."
                ]
            },
            "Bundi": {
                "description": "Bundi, a quaint town in Rajasthan, is known for its beautiful forts, stepwells (baoris), and painted palaces. It retains the charm of an old-world town and offers a glimpse into Rajasthan’s history with its intricate architecture and heritage sites.",
                "activities": [
                    "Visit the Taragarh Fort, a 14th-century fort offering panoramic views of the city and surrounding countryside.",
                    "Explore the Bundi Palace, known for its stunning murals depicting the tales of Radha and Krishna.",
                    "Visit the many baoris (stepwells) such as Raniji ki Baori, which are beautifully carved and have historical significance.",
                    "Take a stroll through the Sukh Mahal, located by the lake, which served as a summer retreat for the royals.",
                    "Walk through the bustling Bundi Bazaar for handicrafts, jewelry, and local artifacts."
                ],
                "must_try_foods": [
                    "Dal Baati Churma, a traditional Rajasthani dish consisting of lentils, baked wheat balls, and a sweet crumble.",
                    "Laapsi, a sweet dish made from broken wheat cooked with ghee and sugar.",
                    "Kachori, a fried pastry filled with spiced lentils, served with chutneys.",
                    "Ghewar, a disc-shaped sweet, often enjoyed during festivals."
                ]
            },
            "Jabalpur": {
                "description": "Jabalpur, located in Madhya Pradesh, is a city known for its stunning natural beauty, marble rock formations, and historical landmarks. It is famous for the Marble Rocks at Bhedaghat and its cultural heritage.",
                "activities": [
                    "Take a boat ride on the Narmada River through the Marble Rocks at Bhedaghat, a unique experience amidst stunning rock formations.",
                    "Visit the Dhuandhar Falls, a powerful waterfall known for its misty spray, often likened to smoke.",
                    "Explore the Madan Mahal Fort, a historical fort with beautiful views of the city.",
                    "Spend time at the Rani Durgavati Museum, which houses sculptures, coins, and artifacts from different periods.",
                    "Visit Chausath Yogini Temple, a 10th-century temple dedicated to Goddess Durga."
                ],
                "must_try_foods": [
                    "Khoye ki Jalebi, a traditional dessert made from milk solids and soaked in sugar syrup.",
                    "Sabudana Khichdi, a light dish made with sago pearls, peanuts, and spices, often enjoyed during fasting.",
                    "Dal Bafla, a wheat-based dish served with spicy lentils, often garnished with ghee.",
                    "Chaat, including pani puri, bhel puri, and other savory street snacks, available at local markets."
                ]
            },
            "Majuli": {
                "description": "Majuli, located in Assam, is the largest river island in the world and is known for its unique cultural heritage and natural beauty. Surrounded by the Brahmaputra River, Majuli is an important center for Vaishnavism and is famous for its serene landscape, tribal culture, and monasteries.",
                "activities": [
                    "Visit the Satras (Vaishnavite monasteries) such as Kamalabari Satra and Auniati Satra to learn about the culture and history.",
                    "Take a ferry ride across the Brahmaputra River and enjoy the scenic views.",
                    "Experience the Raas Leela Festival, a cultural celebration with music, dance, and performances.",
                    "Interact with the Mishing tribe and learn about their traditional way of life.",
                    "Explore the island’s vibrant handicrafts and pottery made by the local artisans."
                ],
                "must_try_foods": [
                    "Pitha, a traditional Assamese rice cake made during festivals.",
                    "Masor Tenga, a tangy fish curry made with tomatoes and lemon, popular in Assamese cuisine.",
                    "Tenga Dal, a sour lentil soup, often served with steamed rice.",
                    "Apong, a traditional rice beer made by the Mishing tribe."
                ]
            },
            "Ranchi": {
                "description": "Ranchi, the capital of Jharkhand, is known for its beautiful waterfalls, rich tribal culture, and natural beauty. It is often called the 'City of Waterfalls' and serves as a gateway to explore the tribal heartland of India.",
                "activities": [
                    "Visit the stunning Dassam Falls and Hundru Falls, popular for their scenic beauty.",
                    "Take in the panoramic views from Tagore Hill, named after the famous poet Rabindranath Tagore.",
                    "Visit the Ranchi Lake and take a boat ride to enjoy the peaceful surroundings.",
                    "Explore the Rock Garden, which offers beautiful views of Kanke Dam.",
                    "Visit the Pahari Mandir, dedicated to Lord Shiva, located atop a hill with a view of the city."
                ],
                "must_try_foods": [
                    "Litti Chokha, a dish made of wheat flour balls filled with gram flour and served with mashed spiced vegetables.",
                    "Thekua, a traditional sweet made with wheat flour, sugar, and dry fruits.",
                    "Chilka Roti, a type of savory pancake made from rice flour and spices.",
                    "Handia, a local rice beer made during festivals and tribal celebrations."
                ]
            },
            "Gulmarg": {
                "description": "Gulmarg, located in Jammu and Kashmir, is a famous hill station known for its snow-capped mountains, ski slopes, and scenic beauty. It’s an ideal destination for adventure seekers and nature lovers, with activities ranging from skiing to gondola rides.",
                "activities": [
                    "Take a ride on the Gulmarg Gondola, one of the highest cable cars in the world, offering breathtaking views.",
                    "Go skiing or snowboarding in the winter, as Gulmarg is one of India’s top ski destinations.",
                    "Visit the beautiful Alpather Lake, located at the base of the Apharwat peak.",
                    "Play a round of golf at the Gulmarg Golf Course, one of the highest golf courses in the world.",
                    "Enjoy a peaceful walk through the meadows of Gulmarg during the summer, surrounded by wildflowers."
                ],
                "must_try_foods": [
                    "Rogan Josh, a flavorful lamb dish cooked with Kashmiri spices.",
                    "Yakhni, a yogurt-based mutton curry that’s mild yet aromatic.",
                    "Kahwa, a traditional Kashmiri tea infused with saffron and almonds.",
                    "Tabak Maaz, lamb ribs simmered in spices and then fried until crispy."
                ]
            },
            "Varanasi": {
                "description": "Varanasi, one of the world's oldest continually inhabited cities, is located on the banks of the Ganges in Uttar Pradesh. Known for its ghats, temples, and spiritual aura, Varanasi is a sacred city for Hindus and a major cultural hub.",
                "activities": [
                    "Attend the mesmerizing Ganga Aarti at Dashashwamedh Ghat during the evening.",
                    "Take an early morning boat ride on the Ganges to witness the beautiful sunrise and rituals along the ghats.",
                    "Visit the ancient Kashi Vishwanath Temple, dedicated to Lord Shiva.",
                    "Explore the narrow lanes of Old Varanasi and shop for silk sarees, handicrafts, and souvenirs.",
                    "Visit Sarnath, where Gautama Buddha delivered his first sermon after enlightenment."
                ],
                "must_try_foods": [
                    "Kachori Sabzi, a popular breakfast dish consisting of fried bread stuffed with lentils and served with spicy vegetable curry.",
                    "Banarasi Paan, a betel leaf preparation that’s famous throughout India.",
                    "Lassi, served in a kulhad (clay pot), rich and refreshing.",
                    "Tamatar Chaat, a spicy, tangy snack made with tomatoes, potatoes, and a variety of spices."
                ]
            },
            "Chandigarh": {
                "description": "Chandigarh, known as 'The City Beautiful,' is the capital of both Punjab and Haryana. Designed by the Swiss-French architect Le Corbusier, Chandigarh is known for its well-planned layout, green spaces, and modern architecture.",
                "activities": [
                    "Visit the Rock Garden, a unique garden created entirely from industrial and home waste.",
                    "Take a boat ride on Sukhna Lake, a beautiful man-made reservoir in the heart of the city.",
                    "Explore the beautiful Rose Garden, home to thousands of varieties of roses and other flowers.",
                    "Admire the architecture of the Capitol Complex, a UNESCO World Heritage site.",
                    "Shop at Sector 17 Market, known for its variety of shops and bustling atmosphere."
                ],
                "must_try_foods": [
                    "Chole Bhature, spicy chickpeas served with fried bread, a favorite dish in Punjab.",
                    "Amritsari Kulcha, a stuffed flatbread typically served with butter and pickle.",
                    "Lassi, a thick yogurt-based drink, often topped with cream or nuts.",
                    "Tandoori Chicken, chicken marinated in spices and cooked in a clay oven, served with mint chutney."
                ]
            },
            "Dwarka": {
                "description": "Dwarka, located in the state of Gujarat, is one of the seven oldest religious cities in India and is part of the Char Dham pilgrimage circuit. It is known for its ancient temples and beautiful coastal views.",
                "activities": [
                    "Visit the famous Dwarkadhish Temple, dedicated to Lord Krishna, and known for its intricate carvings.",
                    "Take a boat ride to Bet Dwarka Island, believed to be the residence of Lord Krishna.",
                    "Explore the Rukmini Devi Temple, dedicated to Lord Krishna's consort.",
                    "Witness the evening aarti at Dwarkadhish Temple for a spiritual experience.",
                    "Walk along Gomti Ghat and visit the nearby temples."
                ],
                "must_try_foods": [
                    "Gujarati Thali, a traditional platter consisting of various curries, breads, rice, and sweets.",
                    "Thepla, a flatbread made with whole wheat flour and fenugreek leaves.",
                    "Khandvi, a savory snack made with gram flour, rolled and garnished with mustard seeds and grated coconut.",
                    "Shrikhand, a sweet yogurt-based dessert flavored with saffron and cardamom."
                ]
            },
            "Chikmagalur": {
                "description": "Chikmagalur, a charming hill station in Karnataka, is known for its lush coffee plantations, misty hills, and beautiful trekking trails. It is a perfect destination for nature lovers and those seeking a peaceful retreat.",
                "activities": [
                    "Visit the Mullayanagiri Peak, the highest peak in Karnataka, for breathtaking views.",
                    "Take a tour of coffee plantations and learn about coffee production.",
                    "Trek to Baba Budangiri, a mountain range known for its scenic views and caves.",
                    "Visit the Hebbe Falls, a stunning waterfall that requires an adventurous ride and trek to reach.",
                    "Explore the ancient Hirekolale Lake during sunset."
                ],
                "must_try_foods": [
                    "Kotte Kadubu, a type of idli steamed in jackfruit leaves, giving it a unique flavor.",
                    "Akki Roti, a flatbread made from rice flour, served with chutney.",
                    "Coffee, freshly brewed from locally grown beans.",
                    "Neer Dosa, a soft, lacy dosa made from rice batter, served with chutney or curry."
                ]
            },
            "Lakshadweep": {
                "description": "Lakshadweep, an archipelago in the Arabian Sea, is known for its turquoise waters, pristine beaches, and vibrant marine life. It is a tropical paradise ideal for those looking to explore untouched beauty and underwater wonders.",
                "activities": [
                    "Go snorkeling or scuba diving in the crystal-clear waters to explore coral reefs.",
                    "Relax on the pristine beaches of Agatti Island or Bangaram Island.",
                    "Take a glass-bottom boat ride to see the colorful marine life without getting wet.",
                    "Explore Kavaratti Island, known for its beautiful lagoons and scenic views.",
                    "Visit the Marine Aquarium to learn about the diverse marine species found in the region."
                ],
                "must_try_foods": [
                    "Tuna Fish Curry, a spicy fish curry cooked with coconut and local spices.",
                    "Coconut Rice, a fragrant rice dish made with grated coconut.",
                    "Fried Fish, freshly caught and fried with local spices.",
                    "Parotta, a layered flatbread served with various curries."
                ]
            },
            "Jodhpur": {
                "description": "Jodhpur, known as the 'Blue City' due to its blue-painted houses, is a vibrant city in Rajasthan. It is famous for its grand palaces, majestic forts, and rich cultural heritage.",
                "activities": [
                    "Visit the imposing Mehrangarh Fort, one of the largest forts in India, with panoramic views of the blue city.",
                    "Explore the Umaid Bhawan Palace, part of which is a luxury hotel, and part is a museum.",
                    "Stroll through the Rao Jodha Desert Rock Park, which showcases the unique flora of the Thar Desert.",
                    "Shop for handicrafts, jewelry, and spices at the bustling Clock Tower Market.",
                    "Visit the Jaswant Thada, a beautiful marble cenotaph built in memory of Maharaja Jaswant Singh."
                ],
                "must_try_foods": [
                    "Dal Baati Churma, a signature Rajasthani dish made with lentils, wheat dumplings, and sweet crumble.",
                    "Mirchi Vada, a spicy snack made with green chilies stuffed with potatoes and deep-fried.",
                    "Makhaniya Lassi, a sweet, thick yogurt drink, perfect for cooling down in the desert heat.",
                    "Gatte Ki Sabzi, gram flour dumplings cooked in a spicy yogurt-based curry."
                ]
            },
            "Mount Abu": {
                "description": "Mount Abu, the only hill station in Rajasthan, is a popular destination known for its cool climate, scenic beauty, and beautiful Jain temples. Nestled in the Aravalli Range, it is a refreshing retreat from the desert heat.",
                "activities": [
                    "Visit the Dilwara Temples, renowned for their exquisite marble carvings and intricate designs.",
                    "Take a boat ride on Nakki Lake and enjoy the serene atmosphere.",
                    "Enjoy panoramic views from Sunset Point, a popular spot for tourists.",
                    "Visit the Guru Shikhar, the highest point in the Aravalli Range, for breathtaking views.",
                    "Explore the Mount Abu Wildlife Sanctuary, home to a variety of flora and fauna."
                ],
                "must_try_foods": [
                    "Rajasthani Thali, a platter that includes dishes like dal, baati, churma, gatte ki sabzi, and more.",
                    "Rabri, a sweet, condensed milk-based dessert flavored with saffron and cardamom.",
                    "Kachori, a fried pastry filled with spiced lentils, often enjoyed as a snack.",
                    "Pani Puri, a popular street food, crispy puris filled with spicy tamarind water."
                ]
            },
            "Lonavala": {
                "description": "Lonavala, a hill station in Maharashtra, is known for its scenic beauty, waterfalls, and lush greenery. It is a popular getaway from Mumbai and Pune, offering a peaceful retreat in the Western Ghats.",
                "activities": [
                    "Visit the famous Bhushi Dam, a popular picnic spot, especially during the monsoon season.",
                    "Explore the Karla Caves and Bhaja Caves, ancient rock-cut Buddhist shrines.",
                    "Trek to Lohagad Fort or Rajmachi Fort for panoramic views of the surrounding hills.",
                    "Enjoy the beautiful Lonavala Lake, surrounded by greenery.",
                    "Shop for chikki, a traditional sweet made from jaggery and nuts."
                ],
                "must_try_foods": [
                    "Chikki, a crunchy sweet made from jaggery and peanuts or other nuts, a specialty of Lonavala.",
                    "Vada Pav, a popular street snack in Maharashtra, made of a spicy potato patty served in a bun.",
                    "Misal Pav, a spicy curry made of sprouts served with bread, garnished with onions, lemon, and sev.",
                    "Bhajiyas, crispy fried fritters, perfect for enjoying with hot tea during the monsoon."
                ]
            },
            "Tirupati": {
                "description": "Tirupati, located in Andhra Pradesh, is one of the most visited pilgrimage destinations in India. It is famous for the Sri Venkateswara Temple, located on the Tirumala hills, which draws millions of devotees each year.",
                "activities": [
                    "Visit the Sri Venkateswara Temple, dedicated to Lord Venkateswara, and take part in the various rituals.",
                    "Explore the Kapila Theertham, a beautiful waterfall located at the base of the Tirumala hills.",
                    "Visit the Sri Kalahasti Temple, known for its intricate carvings and significance in Hindu mythology.",
                    "Trek to Talakona Waterfalls, the highest waterfall in Andhra Pradesh.",
                    "Enjoy the spiritual ambiance of the ISKCON Temple in Tirupati."
                ],
                "must_try_foods": [
                    "Laddu Prasadam, a sweet offered as prasad at the Tirumala temple, famous throughout India.",
                    "Pulihora, a tangy tamarind rice dish, commonly offered in temples.",
                    "Dosas, crispy rice pancakes served with coconut chutney and sambar.",
                    "Pongal, a savory dish made with rice and lentils, often enjoyed for breakfast."
                ]
            },
            "Nainital": {
                "description": "Nainital, a charming hill station in Uttarakhand, is known for its beautiful lakes, scenic views, and pleasant climate. Surrounded by lush hills, it is a popular destination for families and couples.",
                "activities": [
                    "Take a boat ride on the picturesque Naini Lake and enjoy the surrounding hills.",
                    "Visit the Naina Devi Temple, located on the banks of Naini Lake.",
                    "Ride the cable car to Snow View Point for a panoramic view of the Himalayas.",
                    "Stroll along the Mall Road, lined with shops, eateries, and beautiful lake views.",
                    "Trek to Tiffin Top for a picnic and stunning views of the surrounding landscape."
                ],
                "must_try_foods": [
                    "Aloo ke Gutke, a local dish made from boiled potatoes seasoned with local spices.",
                    "Bhatt ki Churkani, a black bean curry that is a Kumaoni specialty.",
                    "Ras, a curry made from lentils, typically served with steamed rice.",
                    "Bal Mithai, a sweet made from khoya and coated with sugar balls."
                ]
            },
            "Mussoorie": {
                "description": "Mussoorie, also known as the 'Queen of the Hills,' is a picturesque hill station in Uttarakhand. It is known for its scenic beauty, colonial heritage, and cool climate, making it a popular getaway for tourists.",
                "activities": [
                    "Take a walk along the Camel's Back Road, offering beautiful views of the mountains.",
                    "Visit the Kempty Falls, a popular picnic spot with a cascading waterfall.",
                    "Ride the cable car to Gun Hill, the second highest peak in Mussoorie, for panoramic views.",
                    "Explore the Mussoorie Mall Road for shopping, dining, and entertainment.",
                    "Visit Lal Tibba, the highest point in Mussoorie, for stunning views of the snow-capped Himalayas."
                ],
                "must_try_foods": [
                    "Aloo ke Gutke, a local potato dish cooked with spices, enjoyed by the residents of Uttarakhand.",
                    "Chole Bhature, a popular North Indian dish served in most eateries in Mussoorie.",
                    "Pahadi Chicken, a traditional spicy chicken curry, often enjoyed with steamed rice.",
                    "Momos, steamed dumplings that are a favorite snack among tourists."
                ]
            },
            "Sundarbans": {
                "description": "The Sundarbans, located in West Bengal, is the largest mangrove forest in the world and a UNESCO World Heritage site. Known for its unique ecosystem, it is home to the famous Royal Bengal Tiger, diverse wildlife, and a network of tidal waterways and islands.",
                "activities": [
                    "Take a boat safari through the mangrove waterways to spot wildlife, including the elusive Royal Bengal Tiger.",
                    "Visit the Sajnekhali Bird Sanctuary to see various species of birds such as kingfishers, herons, and eagles.",
                    "Explore Dobanki Watch Tower for a panoramic view of the forest and observe wildlife from a safe elevation.",
                    "Spend time at Sudhanyakhali Watch Tower, a great place to spot deer, crocodiles, and tigers.",
                    "Interact with the local communities and learn about their unique lifestyle in harmony with the forest."
                ],
                "must_try_foods": [
                    "Bhapa Ilish, steamed hilsa fish cooked with mustard paste, a traditional Bengali delicacy.",
                    "Chingri Malai Curry, prawns cooked in a creamy coconut milk gravy, popular throughout Bengal.",
                    "Panta Bhat, fermented rice served with fried fish and vegetables, often enjoyed during festivals.",
                    "Mocha Ghonto, a traditional dish made from banana flowers, seasoned with Bengali spices."
                ]
            },
            "Kumarakom": {
                "description": "Kumarakom, located in Kerala, is a small village known for its picturesque backwaters, bird sanctuary, and serene landscape. It’s a perfect destination for those looking to relax and experience the natural beauty of Kerala’s waterways.",
                "activities": [
                    "Take a houseboat cruise through the backwaters of Vembanad Lake and enjoy the tranquil environment.",
                    "Visit the Kumarakom Bird Sanctuary, a paradise for bird watchers, where you can spot migratory birds.",
                    "Experience a traditional Ayurvedic massage, offered by local wellness centers.",
                    "Visit the Pathiramanal Island, a small scenic island in Vembanad Lake, accessible by boat.",
                    "Enjoy a canoe ride through the narrow canals to explore village life and the lush landscape."
                ],
                "must_try_foods": [
                    "Karimeen Pollichathu, pearl spot fish marinated with spices, wrapped in banana leaves, and grilled.",
                    "Fish Moilee, a mild coconut-based fish curry, a signature dish in Kerala.",
                    "Appam and Stew, a soft, fluffy rice pancake served with a rich, mildly spiced vegetable or chicken stew.",
                    "Kappa and Meen Curry, boiled tapioca served with spicy fish curry."
                ]
            },
            "Aizawl": {
                "description": "Aizawl, the capital of Mizoram, is a picturesque hill city known for its vibrant culture, scenic landscapes, and cool climate. It offers a peaceful escape from the hustle and bustle of city life, surrounded by lush hills and traditional tribal villages.",
                "activities": [
                    "Visit the Solomon’s Temple, an iconic structure that is a major religious site in Mizoram.",
                    "Explore the Durtlang Hills for breathtaking views of the city and the surrounding landscape.",
                    "Spend time at the State Museum, which showcases Mizo history, culture, and traditions.",
                    "Visit the Reiek Tlang village to experience Mizo culture and enjoy panoramic views of the surrounding hills.",
                    "Explore the bustling Bara Bazaar, a local market offering traditional handicrafts and regional delicacies."
                ],
                "must_try_foods": [
                    "Bai, a popular dish made from boiled vegetables, sometimes mixed with pork or bamboo shoots.",
                    "Vawksa Rep, smoked pork cooked with bamboo shoots and herbs, a staple in Mizo cuisine.",
                    "Arsa Buhchiar, a traditional chicken rice dish, often served during special occasions.",
                    "Zu Tea, a local black tea, often enjoyed in the morning or evening."
                ]
            },
            "Bhubaneswar": {
                "description": "Bhubaneswar, the capital of Odisha, is known as the 'City of Temples' due to its rich history and impressive collection of ancient temples. It is a perfect destination for history enthusiasts, offering a glimpse into India's glorious past through its architecture.",
                "activities": [
                    "Visit the iconic Lingaraj Temple, one of the oldest and most revered temples in Bhubaneswar.",
                    "Explore the Udayagiri and Khandagiri Caves, ancient rock-cut caves with inscriptions and carvings.",
                    "Discover the intricate architecture of the Mukteswara Temple, known as the 'Gem of Odisha'.",
                    "Take a stroll around the Bindu Sagar Lake, a sacred lake surrounded by temples.",
                    "Visit the Nandankanan Zoological Park, a popular zoo that also has a botanical garden and safari."
                ],
                "must_try_foods": [
                    "Chhena Poda, a traditional dessert made of baked cottage cheese with caramelized sugar.",
                    "Pakhala Bhata, fermented rice served with fried vegetables and badi chura, typically enjoyed during the summer.",
                    "Dalma, a lentil-based dish cooked with vegetables, a staple in Odia cuisine.",
                    "Rasagola, a spongy sweet made from chhena, originated in Odisha and is enjoyed all over the state."
                ]
            },
            "Daman": {
                "description": "Daman, located on the western coast of India, is part of the Union Territory of Daman and Diu. It is known for its scenic beaches, colonial architecture, and relaxed atmosphere, making it a popular getaway destination for travelers seeking a coastal retreat.",
                "activities": [
                    "Relax on Jampore Beach, known for its calm waters and scenic views.",
                    "Visit the Moti Daman Fort, which showcases Portuguese colonial architecture and offers a glimpse into Daman's history.",
                    "Explore the Bom Jesus Church, a beautiful old church built during Portuguese rule.",
                    "Take a walk through the Daman Lighthouse and enjoy panoramic views of the Arabian Sea.",
                    "Visit the Devka Beach, a rocky beach with amusement parks and local eateries."
                ],
                "must_try_foods": [
                    "Seafood Platter, including freshly caught fish, prawns, and crabs cooked in a variety of styles.",
                    "Chicken Bullet, a spicy chicken preparation popular among locals.",
                    "Portuguese Wine, reflecting the Portuguese influence on Daman's culture.",
                    "Prawn Curry, a local delicacy cooked with coconut and spices, best enjoyed with rice."
                ]
            },
            "Nagaland": {
                "description": "Nagaland, located in the northeastern part of India, is a land of festivals, rich tribal culture, and scenic landscapes. Known for its vibrant heritage, Nagaland is home to various tribes, each with its unique traditions, attire, and customs.",
                "activities": [
                    "Attend the famous Hornbill Festival held annually in December, showcasing the rich culture, dance, and music of the Naga tribes.",
                    "Visit the Kohima War Cemetery, a memorial dedicated to the soldiers who fought in World War II.",
                    "Explore the traditional Naga Villages like Khonoma, which offer insights into the local culture and sustainable living practices.",
                    "Trek to Dzukou Valley, known for its breathtaking views, lush green hills, and seasonal flowers.",
                    "Discover Kisama Heritage Village, the site of the Hornbill Festival, and learn about the Naga way of life."
                ],
                "must_try_foods": [
                    "Smoked Pork with Bamboo Shoots, a traditional Naga dish flavored with bamboo and spices.",
                    "Axone (Fermented Soybean), used in various dishes to add a unique flavor.",
                    "Anishi, a fermented yam leaf dish commonly cooked with meat.",
                    "Galho, a Naga version of khichdi, made with rice, vegetables, and meat."
                ]
            },
            "Cherrapunji": {
                "description": "Cherrapunji, also known as Sohra, is a town in Meghalaya that is famous for its record-breaking rainfall and lush green landscapes. It is home to many beautiful waterfalls, root bridges, and one of the wettest places on Earth.",
                "activities": [
                    "Visit the famous Nohkalikai Falls, the tallest plunge waterfall in India, offering breathtaking views.",
                    "Trek to the Double Decker Living Root Bridge in Nongriat, a natural marvel formed from the roots of rubber trees.",
                    "Explore the Mawsmai Caves, a network of limestone caves with beautiful stalactites and stalagmites.",
                    "Spend time at Seven Sisters Waterfalls, which offers a stunning view during the monsoon.",
                    "Visit the Eco Park, which provides panoramic views of the surrounding valleys and waterfalls."
                ],
                "must_try_foods": [
                    "Jadoh, a Khasi dish made with rice and meat, seasoned with turmeric and spices.",
                    "Dohneiiong, a pork dish cooked with black sesame seeds.",
                    "Tungrymbai, fermented soybeans cooked with pork and herbs.",
                    "Pumaloi, a type of steamed rice cake, usually enjoyed with vegetables or meat."
                ]
            },
            "Bikaner": {
                "description": "Bikaner, located in the heart of Rajasthan, is known for its majestic forts, vibrant culture, and delicious snacks. The city's architecture, bustling markets, and golden sand dunes give it a unique charm and make it a popular tourist destination.",
                "activities": [
                    "Visit the Junagarh Fort, a magnificent structure with beautiful palaces, courtyards, and balconies.",
                    "Explore the Karni Mata Temple in Deshnoke, also known as the Rat Temple, due to the thousands of rats considered sacred.",
                    "Take a camel safari in the Thar Desert and enjoy the unique landscape of sand dunes.",
                    "Visit the Lalgarh Palace, known for its beautiful architecture and lush gardens.",
                    "Enjoy the Bikaner Camel Festival, held annually, which showcases camel races, dances, and performances."
                ],
                "must_try_foods": [
                    "Bikaneri Bhujia, a spicy fried snack made from gram flour and spices, famous across India.",
                    "Rajasthani Gatta Curry, gram flour dumplings cooked in a tangy yogurt-based gravy.",
                    "Ker Sangri, a traditional desert dish made with dried berries and beans.",
                    "Rabri, a thickened, sweetened milk dish, flavored with cardamom and garnished with nuts."
                ]
            },
            "Bundi": {
                "description": "Bundi, a quaint town in Rajasthan, is known for its beautiful forts, stepwells (baoris), and painted palaces. It retains the charm of an old-world town and offers a glimpse into Rajasthan’s history with its intricate architecture and heritage sites.",
                "activities": [
                    "Visit the Taragarh Fort, a 14th-century fort offering panoramic views of the city and surrounding countryside.",
                    "Explore the Bundi Palace, known for its stunning murals depicting the tales of Radha and Krishna.",
                    "Visit the many baoris (stepwells) such as Raniji ki Baori, which are beautifully carved and have historical significance.",
                    "Take a stroll through the Sukh Mahal, located by the lake, which served as a summer retreat for the royals.",
                    "Walk through the bustling Bundi Bazaar for handicrafts, jewelry, and local artifacts."
                ],
                "must_try_foods": [
                    "Dal Baati Churma, a traditional Rajasthani dish consisting of lentils, baked wheat balls, and a sweet crumble.",
                    "Laapsi, a sweet dish made from broken wheat cooked with ghee and sugar.",
                    "Kachori, a fried pastry filled with spiced lentils, served with chutneys.",
                    "Ghewar, a disc-shaped sweet, often enjoyed during festivals."
                ]
            },
            "Jabalpur": {
                "description": "Jabalpur, located in Madhya Pradesh, is a city known for its stunning natural beauty, marble rock formations, and historical landmarks. It is famous for the Marble Rocks at Bhedaghat and its cultural heritage.",
                "activities": [
                    "Take a boat ride on the Narmada River through the Marble Rocks at Bhedaghat, a unique experience amidst stunning rock formations.",
                    "Visit the Dhuandhar Falls, a powerful waterfall known for its misty spray, often likened to smoke.",
                    "Explore the Madan Mahal Fort, a historical fort with beautiful views of the city.",
                    "Spend time at the Rani Durgavati Museum, which houses sculptures, coins, and artifacts from different periods.",
                    "Visit Chausath Yogini Temple, a 10th-century temple dedicated to Goddess Durga."
                ],
                "must_try_foods": [
                    "Khoye ki Jalebi, a traditional dessert made from milk solids and soaked in sugar syrup.",
                    "Sabudana Khichdi, a light dish made with sago pearls, peanuts, and spices, often enjoyed during fasting.",
                    "Dal Bafla, a wheat-based dish served with spicy lentils, often garnished with ghee.",
                    "Chaat, including pani puri, bhel puri, and other savory street snacks, available at local markets."
                ]
            },
            "Leh": {
                "description": "Leh, located in the Union Territory of Ladakh, is a high-altitude town surrounded by the stunning Himalayan mountains. It is known for its breathtaking landscapes, Buddhist monasteries, and adventurous activities, making it a paradise for travelers.",
                "activities": [
                    "Visit the Thiksey Monastery, a stunning Buddhist monastery known for its architecture and spiritual ambiance.",
                    "Explore the Pangong Lake, famous for its ever-changing hues and serene surroundings.",
                    "Experience the thrill of biking or driving on the Khardung La Pass, one of the highest motorable roads in the world.",
                    "Admire the views from the Leh Palace, a historic nine-story structure overlooking the town.",
                    "Go river rafting on the Zanskar River, an adventure amidst rugged mountain terrains."
                ],
                "must_try_foods": [
                    "Thukpa, a hearty noodle soup with meat or vegetables.",
                    "Momos, steamed dumplings served with spicy chutneys.",
                    "Skyu, a traditional Ladakhi stew made with barley and vegetables.",
                    "Butter Tea, a salty and buttery drink perfect for the cold weather."
                ]
            },
            "Gwalior": {
                "description": "Gwalior, located in Madhya Pradesh, is a city steeped in history and culture. It is known for its stunning palaces, ancient temples, and the majestic Gwalior Fort, which stands as a testament to the city’s rich past. Often referred to as the 'City of Music,' it is also the birthplace of Tansen, the legendary musician.",
                "activities": [
                    "Explore the magnificent Gwalior Fort, which offers panoramic views of the city and houses several historical structures, including the Man Singh Palace and Sas Bahu Temple.",
                    "Visit the Tansen Memorial, a tribute to the great musician and an integral part of the annual Tansen Music Festival.",
                    "Admire the beautiful architecture of Jai Vilas Palace, a grand structure showcasing a blend of European styles and home to the Scindia Museum.",
                    "Walk through the Sun Temple, inspired by the Konark Sun Temple, known for its intricate carvings.",
                    "Enjoy a sound-and-light show at the Gwalior Fort to learn about the city's history in an engaging way."
                ],
                "must_try_foods": [
                    "Bedai with Aloo Sabzi, a popular breakfast dish featuring fried bread served with spicy potato curry.",
                    "Kachoris, deep-fried pastries filled with lentils or spices, served with chutney.",
                    "Poha, a light and flavorful flattened rice dish often garnished with coriander and lemon.",
                    "Gajak, a sweet treat made with sesame seeds and jaggery, perfect for winter."
                ]
            },
            "Ranthambhore": {
                "description": "Ranthambhore, located in Rajasthan, is a renowned wildlife sanctuary and one of the best places in India to spot Bengal tigers in their natural habitat. It is also known for its ancient fort and picturesque landscapes.",
                "activities": [
                    "Take a safari in Ranthambore National Park to spot tigers, leopards, and other wildlife in their natural habitat.",
                    "Visit the Ranthambore Fort, a UNESCO World Heritage site offering panoramic views of the surrounding forest.",
                    "Explore the Padam Talao, a large lake within the park, famous for its serene beauty and the rare sightings of animals near its shores.",
                    "Enjoy birdwatching and capture the beautiful avian species at the Rajbagh Lake.",
                    "Visit the Jogi Mahal, a historic rest house near the edge of Padam Talao."
                ],
                "must_try_foods": [
                    "Laal Maas, a fiery mutton curry cooked with red chilies and traditional Rajasthani spices.",
                    "Gatte Ki Sabzi, gram flour dumplings in a spicy yogurt-based curry.",
                    "Dal Baati Churma, a classic Rajasthani dish of lentils, baked wheat balls, and sweetened crushed wheat.",
                    "Ker Sangri, a unique dish made from desert beans and berries."
                ]
            },
            "Coorg": {
                "description": "Coorg, also known as Kodagu, is a picturesque hill station in Karnataka, often referred to as the 'Scotland of India.' It is known for its lush coffee plantations, misty hills, and serene landscapes, making it a favorite destination for nature lovers and adventure seekers.",
                "activities": [
                    "Explore the coffee plantations and learn about the coffee-making process.",
                    "Visit Abbey Falls, a stunning waterfall surrounded by lush greenery.",
                    "Take a peaceful stroll around Raja's Seat, a garden offering breathtaking views of the valleys.",
                    "Trek to Tadiandamol Peak, the highest peak in Coorg, for panoramic views.",
                    "Visit the Namdroling Monastery (Golden Temple), a beautiful Tibetan monastery in Bylakuppe."
                ],
                "must_try_foods": [
                    "Pandi Curry, a flavorful pork curry made with traditional Coorg spices.",
                    "Akki Roti, rice-based flatbread often served with spicy chutneys.",
                    "Kadambuttu, steamed rice dumplings served with curries.",
                    "Coorg Coffee, freshly brewed coffee from the local plantations.",
                    "Noolputtu, rice noodles typically served with meat or vegetable curry."
                ]
            },

        }

    
        df['Health Conditions'] = df['Health Conditions'].apply(
            lambda x: x.split(", "))
        df['Activity Type'] = df['Activity Type'].apply(
            lambda x: x.split(", "))

        # MultiLabelBinarizer for health conditions and activity type
        mlb_health = MultiLabelBinarizer()
        mlb_activity = MultiLabelBinarizer()
        df_health_encoded = pd.DataFrame(mlb_health.fit_transform(
            df['Health Conditions']), columns=mlb_health.classes_)
        df_activity_encoded = pd.DataFrame(mlb_activity.fit_transform(
            df['Activity Type']), columns=mlb_activity.classes_)

        #  the encoded fields with the original DataFrame
        df_encoded = pd.concat(
            [df, df_health_encoded, df_activity_encoded], axis=1)

        # One-hot encode categorical features
        df_encoded = pd.get_dummies(df_encoded, columns=[
                                    'Gender', 'Climate Preference', 'Travel Budget', 'Time Available', 'Travel Companions'], drop_first=True)

     
        df_encoded.drop(['UserID', 'Health Conditions', 'Activity Type',
                        'Recommended Place', 'Current Location'], axis=1, inplace=True)

   
        user_profile = {col: 0 for col in df_encoded.columns}


        for condition in health_conditions:
            if condition in user_profile:
                user_profile[condition] = 1

        for activity in activity_type:
            if activity in user_profile:
                user_profile[activity] = 1

        if f'Gender_{gender}' in user_profile:
            user_profile[f'Gender_{gender}'] = 1
        if f'Climate Preference_{climate_preferences}' in user_profile:
            user_profile[f'Climate Preference_{climate_preferences}'] = 1
        if f'Travel Budget_{travel_budget}' in user_profile:
            user_profile[f'Travel Budget_{travel_budget}'] = 1
        if f'Time Available_{time_available}' in user_profile:
            user_profile[f'Time Available_{time_available}'] = 1
        if f'Travel Companions_{travel_companions}' in user_profile:
            user_profile[f'Travel Companions_{travel_companions}'] = 1

      
        user_df = pd.DataFrame([user_profile])

       
        cosine_sim = cosine_similarity(user_df, df_encoded).flatten()
       

    
        top_indices = cosine_sim.argsort()[-10:][::-1]
        recommended_places = df.iloc[top_indices]['Recommended Place'].values
        similarity_scores = cosine_sim[top_indices]  # These are the similarity scores for the top 10 places


        print("Top 10 Recommended Places and their Cosine Similarity Scores:")
        for place, score in zip(recommended_places, similarity_scores):
            print(f"Place: {place}, Similarity Score: {score}")
        


   
        recommendations = [
            {
                'place': place,
                'description': place_details.get(place, {}).get('description', "Description not available."),
                'activities': place_details.get(place, {}).get('activities', []),
                'must_try_foods': place_details.get(place, {}).get('must_try_foods', [])
            }
            for place in recommended_places
        ]

        return render(request, 'result.html', {'recommendations': recommendations, 'login': login})

    return render(request, 'recommend.html', {'login': login})
