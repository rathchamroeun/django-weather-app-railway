from django.shortcuts import redirect, render
import requests
from .models import City
from django.contrib import messages


def home(request):
    API_KEY = 'c4895700bbab6bd0c0488c86633c6308'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    if request.method == 'POST':
        city_name = request.POST.get('city')

        response = requests.get(url.format(city_name, API_KEY)).json()

        if response['cod'] == 200:
            if not City.objects.filter(name = city_name).exists():

                City.objects.create(name=city_name)
                messages.success(request, f'{city_name} has been added successfully.')
            else:
                messages.info(request, f'{city_name} already exists in the database.')
        else:           
             messages.error(request, f'{city_name} is not found.')

        return redirect('home')

    weather_data = []

    try:
        cities = City.objects.all()

        for city in cities:
            response = requests.get(url.format(city.name, API_KEY))
            data = response.json()

            if data['cod'] == 200:
                weather = {
                    'city': city.name,
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                }

                weather_data.append(weather)

            else:
                City.objects.filter(name=city.name).delete()

    except requests.RequestException as e:
        print('Error connecting to the API:', e)

    context = {'weather_data': weather_data}

    return render(request, 'index.html', context)