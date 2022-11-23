from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'customers/index.html')

def listCoach(request):
    return render(request, 'customers/listCoach.html')