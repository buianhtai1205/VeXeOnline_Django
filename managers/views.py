from .models import Trip, Garage, Manager, Seat, Schedule, Ticket
from customers.models import Customer
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

# Index
def index(request):
  email=''
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
    garage = manager.garage
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  listTrips = Trip.objects.all().values()
  listSchedules = Schedule.objects.filter(garage=garage)
  template = loader.get_template('managers/index.html')
  context = {
    'listTrips': listTrips,
    'manager':manager,
    'listSchedules':listSchedules,
    'garage':garage,
    'trip':listTrips[0]
  }
  return HttpResponse(template.render(context, request))


#trip
def addtrip(request):
  template = loader.get_template('managers/addTrip.html')
  return HttpResponse(template.render({}, request))

def addrecordtrip(request):
  departure = request.POST['departure']
  destination = request.POST['destination']
  price = request.POST['price']
  num_seat = request.POST['num_seat']
  garageNum = request.POST['garage_id']
  departure_time = request.POST['departure_time']
  garage = Garage.objects.get(id=garageNum)
  trip = Trip(departure= departure, destination = destination, price= price, num_seat = num_seat, garage = garage,departure_time = departure_time )
  trip.save()
  for i in range(0,int(num_seat)):
    seat = Seat(number_chair = i,trip = trip, status = 0)
    seat.save()
  return HttpResponseRedirect(reverse('managers:index'))

def viewTrip(request,id):
  email=''
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  trip = Trip.objects.get(id=id)
  listSeats= Seat.objects.filter(trip = trip)
  garage = manager.garage
  listSchedules = Schedule.objects.filter(garage=garage)
  template = loader.get_template('managers/viewTrip.html')
  context = {
    'listSeats': listSeats,
    'manager':manager,
    'listSchedules':listSchedules,
    'trip':trip
  }
  return HttpResponse(template.render(context, request))
def edittrip(request, id):
  trip = Trip.objects.get(id=id)
  context = {
    'trip': trip,
  }
  template = loader.get_template('managers/editTrip.html')
  return HttpResponse(template.render(context, request))

def editrecordtrip(request, id):
  trip = Trip.objects.get(id=id)
  trip.departure = request.POST['departure']
  trip.destination = request.POST['destination']
  trip.price = request.POST['price']
  trip.num_seat = request.POST['num_seat']
  garageNum = request.POST['garage_id']
  trip.departure_time = request.POST['departure_time']
  trip.garage = Garage.objects.get(id=garageNum)
  trip.save()
  return HttpResponseRedirect(reverse('managers:index'))

def deletetrip(request, id):
  trip = Trip.objects.get(id=id)
  trip.delete()
  return HttpResponseRedirect(reverse('managers:index'))


#Manager
def managerLogin(request):
  template = loader.get_template('managers/managerLogin.html')
  return HttpResponse(template.render({}, request))

def managerLoginRecord(request):
  email = request.POST['email']
  password = request.POST['password']
  try:
    manager = Manager.objects.get(email=email, password = password)
    request.session['email'] = manager.email
  except Manager.DoesNotExist:
    comment = 'Tài khoản hoặc mật khẩu không chính xác'
    context = {
    'comment': comment,
    }
    template = loader.get_template('managers/managerLogin.html')
    return HttpResponse(template.render(context, request))
  
  return HttpResponseRedirect(reverse('managers:index'))

def managerSignup(request):
  template = loader.get_template('managers/managerSignUp.html')
  return HttpResponse(template.render({}, request))

def managerSignUpRecord(request):
  template = loader.get_template('managers/managerSignUp.html')
  email = request.POST['email']
  password = request.POST['password']
  phone = request.POST['phone']
  fullName = request.POST['fullName']
  confirmPassword = request.POST['confirmPassword']
  if(email == '' or password=='' or phone=='' or fullName =='' or confirmPassword==''):
    comment = 'Hãy nhập các thông tin cần thiết'
    context = {
    'comment': comment,
    }
    return HttpResponse(template.render(context, request))
  if(password!=confirmPassword):
    comment = 'Mật khẩu và nhập lại mật khẩu không trùng nhau'
    context = {
    'comment': comment,
    }
    return HttpResponse(template.render(context, request))
  try:
    manager = Manager.objects.get(email=email)
    comment = 'Email đã tồn tại'
    context = {
    'comment': comment,
    }
    return HttpResponse(template.render(context, request))
  except Manager.DoesNotExist:
    garade = Garage()
    garade.save()
    manager =  Manager(email = email, password = password, phoneNumber = phone, fullName = fullName, garage = garade)
    manager.save()
    comment = 'Tài khoản đã được tạo. Hãy đăng nhập'
    context = {
    'comment': comment,
    }
    template1 = loader.get_template('managers/managerLogin.html')
    return HttpResponse(template1.render(context, request))

def editProfile(request):
  email=''
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  template = loader.get_template('managers/editProfile.html')
  context = {
    'manager':manager,
  }
  return HttpResponse(template.render(context, request))


def editProfileRecord(request):
  email=''
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  manager.fullName = request.POST['fullName']
  manager.phoneNumber = request.POST['phone']
  manager.save()
  return HttpResponseRedirect(reverse('managers:index'))

def editPassword(request):
  email=''
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  template = loader.get_template('managers/editPassword.html')
  return HttpResponse(template.render({}, request))

def editPasswordRecord(request):
  email=''
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  template = loader.get_template('managers/editPassword.html')
  password = request.POST['oldPass']
  newPass = request.POST['newPass']
  confirmPassword = request.POST['confirmPass']
  if(newPass == '' or password=='' or confirmPassword==''):
    comment = 'Hãy nhập các thông tin cần thiết'
    context = {
    'comment': comment,
    }
    return HttpResponse(template.render(context, request))
  if(newPass!=confirmPassword):
    comment = 'Mật khẩu và nhập lại mật khẩu không trùng nhau'
    context = {
    'comment': comment,
    }
    return HttpResponse(template.render(context, request))
  if(manager.password!=password):
    comment = 'Sai mật khẩu cũ'
    context = {
    'comment': comment,
    }
    return HttpResponse(template.render(context, request))
  manager.password = newPass
  manager.save
  comment = 'Đổi mật khẩu thành công'
  context = {
    'comment': comment,
    }
  return HttpResponse(template.render(context, request))


#Garage
def editGarage(request):
  email=''
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  template = loader.get_template('managers/editGarage.html')
  context={
    'garage':manager.garage
  }
  return HttpResponse(template.render(context, request))

def editGarageRecord(request):
  email=''
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  template = loader.get_template('managers/editGarage.html')
  fullName = request.POST['fullName']
  address = request.POST['address']
  description = request.POST['description']
  if(fullName == '' or address=='' or description==''):
    comment = 'Hãy nhập các thông tin cần thiết'
    context = {
    'comment': comment,
    }
    return HttpResponse(template.render(context, request))
  garage = manager.garage
  garage.fullName = fullName
  garage.address = address
  garage.description = description
  garage.save()
  comment = 'Đổi thông tin thành công'
  context = {
    'comment': comment,
    }
  return HttpResponse(template.render(context, request))


#Seat
def viewSeat(request,id):
  email=''
  template = loader.get_template('managers/viewSeat.html')
  context={}
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
    seat = Seat.objects.get(id=id)
    trip = seat.trip
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  try:
    ticket = Ticket.objects.get(seat = seat, trip= trip)
    customer = Customer.objects.get(id=ticket.customer.id)
    context = {
    'seat': seat,
    'manager':manager,
    'trip':trip,
    'customer':customer,
    'ticket':ticket,
    }
    return HttpResponse(template.render(context, request))
  except Ticket.DoesNotExist:
    ticket = Ticket()
  context = {
    'seat': seat,
    'manager':manager,
    'trip':trip,
    'ticket':ticket,
  }
  return HttpResponse(template.render(context, request))


#Schedule
def addSchedule(request):
  email=''
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  template = loader.get_template('managers/addSchedule.html')
  listTrip = Trip.objects.filter(garage = manager.garage)
  context = {
    'manager':manager,
    'trip':listTrip[0],
  }
  return HttpResponse(template.render(context, request))

def addScheduleRecord(request):
  email=''
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  musty = request.POST['musty']
  status = request.POST['status']
  garage = manager.garage
  schedule = Schedule(musty=musty, garage=garage, status=status)
  schedule.save() 
  return HttpResponseRedirect(reverse('managers:index'))

def deleteSchedule(request, id):
  email=''
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  schedule = Schedule.objects.get(id=id)
  schedule.delete()
  return HttpResponseRedirect(reverse('managers:index'))


#Revenue
def managerRevenue(request):
  email=''
  try:
    email = request.session['email']
    manager = Manager.objects.get(email = email)
    garage = manager.garage
  except KeyError:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  except Manager.DoesNotExist:
    return HttpResponseRedirect(reverse('managers:managerLogin'))
  template = loader.get_template('managers/managerRevenue.html')
  context = {
    'manager':manager,
  }
  return HttpResponse(template.render(context, request))