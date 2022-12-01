from django.test import TestCase
from managers.models import Trip


from django.http import HttpResponse
from django.core import serializers

# Create your tests here.
def index(request):
    departure = Trip.objects.distinct().values('departure')
    destination = Trip.objects.distinct().values('destination')
    data = serializers.serialize('json', departure)
    return HttpResponse(data, content_type="application/json")
