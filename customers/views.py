from django.shortcuts import render
from managers.models import Trip


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
    # data = serializers.serialize('json', list_trip)
    # return HttpResponse(data, content_type='application/json')
    return render(request, 'customers/listCoach.html', {'list_trip': list_trip})  