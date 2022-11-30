from django.shortcuts import render
from managers.models import Trip
from managers.models import Seat
from managers.models import Schedule

from django.http import HttpResponse
from django.core import serializers

# Create your views here.
def index(request):
    departure = Trip.objects.distinct().values('departure')
    destination = Trip.objects.distinct().values('destination')
    return render(request, 'customers/index.html', {'departure': departure, 'destination': destination})

def listCoach(request):
    if request.method == 'POST':
        data = request.POST.dict()
        departure = data['departure']
        destination = data['destination']
        departure_time = data['departure_time']
    list_trip = Trip.objects.all().filter(departure = departure, destination = destination, departure_time__date = departure_time).prefetch_related()
    data = serializers.serialize('json', list_trip)
    import json
    data_dict = json.loads(data)
    detail = {}
    for item in data_dict:
        list_seat = Seat.objects.all().filter(trip_id = item['pk']).values('id', 'number_chair', 'status')
        list_musty = Schedule.objects.all().filter(garage_id = item['fields']['garage']).values()
        detail[item['pk']] = {
            'list_seat': list_seat,
            'list_musty': list_musty,
        }
    # return HttpResponse(detail[1]['list_seat'][0]['number_chair'], content_type='application/json')
    return render(request, 'customers/listCoach.html', {'list_trip': list_trip, 'detail': detail})  