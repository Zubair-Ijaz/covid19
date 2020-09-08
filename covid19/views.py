from django.http import JsonResponse
from django.shortcuts import render

import requests
import json
import locale
import dateutil.parser
import datetime

data1 = []
def home(request):
    response = requests.get('https://covid19.mathdro.id/api')
    json_data = json.loads(response.text)
    resp = requests.get('https://covid19.mathdro.id/api/countries')
    country_data = json.loads(resp.text)
    countries = country_data['countries']
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
    iso2 = 'Globe'
    if request.method == 'POST':
        iso2 = request.POST['droped']
        if iso2 == 'Globe':
            response = requests.get('https://covid19.mathdro.id/api')
            json_data = json.loads(response.text)
        else:
            response = requests.get('https://covid19.mathdro.id/api/countries/'+iso2)
            json_data = json.loads(response.text)

    confirmed = json_data['confirmed']['value']
    recovered = json_data['recovered']['value']
    deaths = json_data['deaths']['value']
    active = (confirmed - (recovered + deaths))
    date = json_data['lastUpdate']
    date = dateutil.parser.isoparse(date)
    date = date.strftime('%a %b %d %Y')

    data = [
        ['Infected', f'{confirmed:n}', date, 'Number of infected people from COVID-19', 'infected'],
        ['Recovered', f'{recovered:n}', date, 'Number of recoveries from COVID-19', 'recovered'],
        ['Active', f'{active:n}', date, 'Number of active cases of COVID-19', 'active'],
        ['Deaths', f'{deaths:n}', date, 'Number of deaths caused by COVID-19', 'death']
    ]
    
    global data1
    data1 = {
        'values': [confirmed, recovered, active, deaths],
        'country': iso2
    }
    context = {
        'data': data,
        'countries': countries,
        'iso2': iso2,
    }
    
    return render(request, 'home.html', context)

def chart_data(request):
    global data1
    labels = ['Infected', 'Recovered', 'Active', 'Deaths']
    chartLabel = "Current state in "
    chartdata = [data1['values'][0], data1['values'][1], data1['values'][2], data1['values'][3]]
    data ={ 
        "labels":labels, 
        "chartLabel":chartLabel, 
        "chartdata":chartdata, 
    } 
    return JsonResponse(data)

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request, exception):
    return render(request, '500.html', status=500)