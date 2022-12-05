
from django.http import HttpResponse
from .models import Customer
from managers.models import Ticket,Trip,Seat,Garage
from django.urls import reverse
from django.db import transaction,IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import random 
import string
from datetime import datetime
# import phonenumbers
# Create your views here.
def index(request):
   return render(request, 'customers/index.html')

def loginView(request):
   return render(request, 'customers/login_view.html')

def quanlyveView(request):
   content = quanlyveInfo(request)
   return render(request, 'customers/quanlyveView.html',content)

def userInfo(request):
   content = {}
   if 'fullname' in request.session:
        if (request.session['fullname']):
            fullname = request.session['fullname']
            content['fullname'] = fullname
   if 'email' in request.session:
        if (request.session['email']):
            email = request.session['email']
            content['email'] = email
   if 'numberPhone' in request.session:
        if (request.session['numberPhone']):
            numberPhone = request.session['numberPhone']
            content['numberPhone'] = numberPhone
   return render(request, 'customers/userInfo.html',content)

@csrf_exempt
def checkCustomer(request):
    if request.method == 'POST':
            login_data = request.POST.dict()
            numberPhone = login_data['numberPhone']
            password = login_data['password']
            num_rows = Customer.objects.filter(phoneNumber=numberPhone, password=password).count()
            nameUser=None
            emailUser = None
            sql = "SELECT * FROM customers_customer where phoneNumber =" + numberPhone
            User = Customer.objects.raw(sql)
            for data in User:
                nameUser=data.fullName
                emailUser=data.email
            if num_rows > 0:
                request.session['numberPhone'] = numberPhone
                request.session['fullname'] = nameUser
                request.session['email'] = emailUser
                messages = "Đăng nhập thành công!"
                content = {'numberPhone': numberPhone, 'messages': messages}
            
                return redirect(reverse('customers:userInfo', kwargs = {}))
            else:
                messages = "Số điện thoại hoặc mật khẩu không đúng!"
                content = {'messages': messages}
                return render(request, 'customers/login_view.html',content)
    return HttpResponse("Sai method")

@csrf_exempt
def forgotPassword(request):
    if request.method == 'POST':
        login_data = request.POST.dict()
        numberPhone = login_data['numberPhoneForgotPassword']
        num_rows = Customer.objects.filter(phoneNumber=numberPhone).count()
        if num_rows > 0:
            _password = _pw(8)
            updatePassword = "UPDATE customers_customer  SET password = "+ _password  + "WHERE phoneNumber = " + numberPhone
            Customer.objects.raw(updatePassword)
            sql = "SELECT * FROM customers_customer where phoneNumber =" + numberPhone
            User = Customer.objects.raw(sql)
            for data in User:
                nameUser=data.fullName
                emailUser=data.email
                passwordNew = data.password
            messages = "Đã đổi mật khẩu thành công!"
            content = {'numberPhone': numberPhone, 'messages': messages}
            data = "Xin chào: " + nameUser+ " chúng tôi vừa cập nhật lại mật khẩu cho bạn, mật khẩu mới là: " + passwordNew
            send_mail('Welcome!', data, "PLC", [emailUser], fail_silently=False)
            return render(request, 'customers/success.html')
        else:
            messages = "Số điện thoại không đúng!"
            content = {'messages': messages}
            return render(request, 'customers/login_view.html',content)
    return HttpResponse("Sai method")
    

# def listCoach(request):
#     return render(request, 'customers/listCoach.html')

@csrf_exempt
def datve(request):
  if request.method == 'POST':
    idChuyen = request.POST.get('inputIdChuyenXe', '')
    idGhe = request.POST.get('gheDangChon', '')
    tenKh = request.POST.get('nameUser', '')
    phoneUser = request.POST.get('phoneUser', '')
    email = request.POST.get('emailUser', '')
    password = _pw(8)

    sid = transaction.savepoint()
    # add Customer
    kh =  Customer()
    kh.fullName = tenKh
    kh.phoneNumber = phoneUser
    kh.email = email
    kh.password = password
    kh.save()

    # add Ticket
    sql = "SELECT id from customers_customer where phoneNumber = " + phoneUser
    User = Customer.objects.raw(sql)
    for data in User:
        idUser=data.id

    _idChuyen = idChuyen
    _idSeat = idGhe
    _idCustomer= idUser

    if(_idSeat != None):
        ticket = Ticket()
        ticket.trip_id = _idChuyen
        ticket.seat_id = _idSeat
        ticket.customer_id = _idCustomer
        ticket.save() 
    data = "Chuyến số: " + idChuyen + " \nGhế số: " + idGhe + " \nĐịa điểm đón: "  + " \nĐịa điểm trả: " + "\nTài khoản để đăng nhập để kiểm tra vé là: Tên đăng nhập: " + phoneUser +" " + "Mật khẩu: "+ password;
    send_mail('Welcome!', data, "PLC", [email], fail_silently=False)
    if IntegrityError:
            transaction.savepoint_rollback(sid)
    else:
            try:
                transaction.savepoint_commit(sid)
            except IntegrityError:
                transaction.savepoint_rollback(sid)
    return render(request, 'customers/success.html')
  return HttpResponse("Sai method")

def _pw(length=8):
    s = ''
    for i in range(length):
        s += random.choice(string.digits)
    return s

def getTripByTicket(request,phoneNumber):
    idTrip = "SELECT 1 as id, managers_ticket.trip_id,managers_ticket.seat_id from managers_ticket join customers_customer on customers_customer.id = managers_ticket.customer_id where phoneNumber = " + phoneNumber;
    _Trip = Ticket.objects.raw(idTrip)
    # getTrip
    for data in _Trip:
        trip_id=data.trip_id
        seat_id=data.seat_id
    trip = "SELECT * from managers_trip where managers_trip.id =" + str(trip_id);
    _getTrip = Trip.objects.raw(trip)
    for data in _getTrip:
        departure= data.departure
        destination=data.destination
        departure_time=data.departure_time
        price=data.price
        garage_id=data.garage_id
        # getGarage 
        idGarage = "SELECT * FROM managers_garage WHERE id = " + str(garage_id);
        _Garage = Garage.objects.raw(idGarage)
        for data in _Garage:
            fullnameGarage=data.fullName
            description=data.description
        # getSeat 
        seat = "SELECT * FROM Seat WHERE id = " + str(seat_id);
        _Seat = Seat.objects.raw(idGarage)
        for data in _Seat:
            number_chair=data.number_chair
            # status=data.status
        request.session['departure'] = departure
        request.session['destination'] = destination
        request.session['departure_time'] = str(departure_time)
        request.session['price'] = price
        request.session['fullnameGarage'] = fullnameGarage
        request.session['description'] = description
        request.session['number_chair'] = number_chair
        # request.session['status'] = status
        
def quanlyveInfo(request):
   content = {}
   if 'departure' in request.session:
        if (request.session['departure']):
            departure = request.session['departure']
            # email = request.session['email']
            content['departure'] = departure
            # content['email'] = email
   if 'destination' in request.session:
        if (request.session['destination']):
            destination = request.session['destination']
            # email = request.session['email']
            content['destination'] = destination
            # content['email'] = email
   if 'departure_time' in request.session:
        if (request.session['departure_time']):
            departure_time = request.session['departure_time']
            content['departure_time'] = departure_time
   if 'price' in request.session:
        if (request.session['price']):
            price = request.session['price']
            content['price'] = price
   if 'fullnameGarage' in request.session:
        if (request.session['fullnameGarage']):
            fullnameGarage = request.session['fullnameGarage']
            content['fullnameGarage'] = fullnameGarage
   if 'description' in request.session:
        if (request.session['description']):
            description = request.session['description']
            content['description'] = description
   if 'number_chair' in request.session:
        if (request.session['number_chair']):
            number_chair = request.session['number_chair']
            content['number_chair'] = number_chair
   return content

    
    

    
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
    detail = []
    for item in data_dict:
        list_seat = Seat.objects.all().filter(trip_id = item['pk']).values('id', 'number_chair', 'status')
        list_musty = Schedule.objects.all().filter(garage_id = item['fields']['garage']).values()
        trip_id = item['pk']
        detail.append ({
            'trip_id': trip_id,
            'list_seat': list_seat,
            'list_musty': list_musty,
        })
    # return HttpResponse(detail[1]['list_seat'][0]['number_chair'], content_type='application/json')
    return render(request, 'customers/listCoach.html', {'list_trip': list_trip, 'detail': detail})  
