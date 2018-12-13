from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
import requests
import json
from .models import City
from .forms import CityForm
import datetime
from django.contrib import messages

def index(request):
    '''This is your home page'''
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=7b88962e8e99c4170549bcfefdd7a29d' #current-weather
    url2 = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=imperial&APPID=7b88962e8e99c4170549bcfefdd7a29d'  #five-day

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()

    form = CityForm()
    cities = City.objects.all()

    def time_converter(time):
        '''Converts the time'''
        converted_time = datetime.datetime.fromtimestamp(
            int(time)
        ).strftime('%I:%M %p')
        return converted_time

    def get_queryset(self):
        return City.objects.all()

    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        r2 = requests.get(url2.format(city)).json()

        city_weather = {
            'city' : city.name,
            'country' : r['sys']['country'],
            'temperature' : r['main']['temp'],
            'max' : r['main']['temp_max'],
            'min' : r['main']['temp_min'],
            'cloud' : r['clouds']['all'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
            'humidity' : r['main']['humidity'],
            'pressure' : r['main']['pressure'],
            'wind' : r['wind']['speed'],
            'sunrise' : time_converter(r['sys']['sunrise']),
            'sunset' : time_converter(r['sys']['sunset']),
            'dtime' : time_converter(r['dt']),
            }

        current_date=''
        date_list=[]
        day_list=[]
        time_list=[]
        temp_list=[]
        for item in r2['list']:
            time = item['dt_txt']
            temp = item['main']['temp']
            next_date, hour = time.split(' ')
            if current_date != next_date:
                current_date = next_date
                year, month, day = current_date.split('-')
                date_dict = {'y': year, 'm': month, 'd': day}
                date_var = '{m}/{d}/{y}'.format(**date_dict)
                day_var = datetime.datetime.strptime('{m}/{d}/{y}'.format(**date_dict), '%m/%d/%Y').strftime('%A')
                date_list.append(date_var)
                day_list.append(day_var)

            hour = int(hour[:2])
            if hour < 12:
                if hour == 0:
                    hour = 12
                meridiem = 'AM'
            else:
                if hour > 12:
                    hour -= 12
                meridiem = 'PM'

            # Prints the hours [HH:MM AM/PM]
            time_var = '\n%i:00 %s' % (hour, meridiem)
            temp_var = '{}'.format(temp)
            time_list.append(time_var)
            temp_list.append(temp_var)
        keys = range(6)
        keys2 = range(40)
        date_dict = dict(zip(keys,date_list))
        day_dict = dict(zip(keys,day_list))
        time_dict = dict(zip(keys2,time_list))
        temp_dict = dict(zip(keys2,temp_list))

        city_weather['date']=date_dict
        city_weather['day']=day_dict
        city_weather['time']=time_dict
        city_weather['temp']=temp_dict

        weather_data.append(city_weather)
    print(weather_data)
    context = {'weather_data' : weather_data, 'form' : form}
    return render(request,'weather/index.html', context)

def delete(request,id):
    '''Deletes the weather card'''
    obj = City.objects.get(pk=id)
    obj.delete()
    messages.success(request,('Item has been deleted'))
    return redirect('weather_app:index',permanent=True)
