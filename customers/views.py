
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
number_chair1=""
number_chair2=""
number_chair3=""
def index(request):
   return render(request, 'customers/index.html')

def loginView(request):
   return render(request, 'customers/login/login_view_notify.html')

def quanlyveView(request):
   content = quanlyveInfo(request)
   return render(request, 'customers/user_info/quanlyveView.html',content)

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
   return render(request, 'customers/user_info/userInfo.html',content)

@csrf_exempt
def checkCustomer(request):
    if request.method == 'POST':
            login_data = request.POST.dict()
            numberPhone = login_data['numberPhone']
            password = login_data['password']
            num_rows = Customer.objects.filter(phoneNumber=numberPhone, password=password).count()
            nameUser=""
            emailUser = ""
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
                getTripByTicket(request,numberPhone)
                content = {'numberPhone': numberPhone, 'messages': messages}
                return redirect(reverse('customers:userInfo', kwargs = {}))
            else:
                messages = "Số điện thoại hoặc mật khẩu không đúng!"
                content = {'messages': messages}
                return render(request, 'customers/login/login_view.html',content)
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
            return render(request, 'customers/login/login_view_notify.html',content)
    return HttpResponse("Sai method")
    

# def listCoach(request):
#     return render(request, 'customers/listCoach.html')

@csrf_exempt
def datve(request):
  if request.method == 'POST':
    data = request.POST.dict()
    idChuyen = request.POST.get('inputIdChuyenXe', '')
    idGhe1 = request.POST.get('seatID1', '')
    idGhe2 = request.POST.get('seatID2', '')
    idGhe3 = request.POST.get('seatID3', '')
    diemDon = request.POST.get('checkbox', '')
    diemTra = request.POST.get('_checkbox', '')
    tenKh = data['nameUser'+ str(1)]
    phoneUser = data['phoneUser'+ str(1)]
    email = data['emailUser'+ str(1)]
    password = _pw(8)
    sid = transaction.savepoint()
    # add Customer
    if idChuyen != "" and diemDon != "" and diemTra != "":
        kh =  Customer()
        kh.fullName = tenKh
        kh.phoneNumber = phoneUser
        kh.email = email
        kh.password = password
        kh.save()

    # add Ticket
        sqlDiemDon = "SELECT id,musty from managers_schedule where id = " + str(diemDon)
        _Schedule = Schedule.objects.raw(sqlDiemDon)
        for data in _Schedule:
            mustyDon=data.musty

        sqlDiemTra = "SELECT id,musty from managers_schedule where id = " + str(diemTra)
        _Schedule = Schedule.objects.raw(sqlDiemTra)
        for data in _Schedule:
            mustyTra=data.musty

        sql = "SELECT id from customers_customer where phoneNumber = " + str(phoneUser)
        User = Customer.objects.raw(sql)
        for data in User:
            idUser=data.id
        
        _idChuyen = idChuyen
        _idSeat1 = idGhe1
        _idSeat2 = idGhe2
        _idSeat3 = idGhe3
        _idCustomer= idUser
        _diemDon= diemDon

        if(_idSeat1 != "" and _idChuyen != "" and _diemDon != "" and _idCustomer != ""):
          
            if _idSeat1 != "" :
                ticket = Ticket()
                ticket.trip_id = _idChuyen
                ticket.seat_id = _idSeat1
                ticket.customer_id = _idCustomer
                ticket.schedule_id = _diemDon
                ticket.save() 

                seat = "SELECT * FROM managers_seat WHERE id = " + str(idGhe1)
                _Seat = Seat.objects.raw(seat)
                for data in _Seat:
                    number_chair1=data.number_chair
            if  _idSeat2 != "" :
                ticket = Ticket()
                ticket.trip_id = _idChuyen
                ticket.seat_id = _idSeat2
                ticket.customer_id = _idCustomer
                ticket.schedule_id = _diemDon
                ticket.save() 
                
                seat = "SELECT * FROM managers_seat WHERE id = " + str(idGhe2)
                _Seat = Seat.objects.raw(seat)
                for data in _Seat:
                    number_chair2=data.number_chair
            if _idSeat3 != "":
                ticket = Ticket()
                ticket.trip_id = _idChuyen
                ticket.seat_id = _idSeat3 
                ticket.customer_id = _idCustomer
                ticket.schedule_id = _diemDon
                ticket.save() 
                
                seat = "SELECT * FROM managers_seat WHERE id = " + str(idGhe3)
                _Seat = Seat.objects.raw(seat)
                for data in _Seat:
                    number_chair3=data.number_chair
           
            trip = "SELECT * from managers_trip where managers_trip.id =" + str(_idChuyen);
            _getTrip = Trip.objects.raw(trip)
            for data in _getTrip:
                departure= data.departure
                destination=data.destination
                departure_time=data.departure_time
                price=data.price

            data = "Xin chào bạn: Cảm ơn bạn đã đặt vé bên công ty chúng tôi, đây là thông tin vé của bạn :\nGhế số: " + number_chair1 + " " + number_chair2 +"" +  str(number_chair3) + " \nĐịa điểm đón: "  + str(mustyDon) + " " + destination +  " \nĐịa điểm trả: " + str(mustyTra) +" " +  departure + "\nGiờ khởi hành: " + str(departure_time) + "\nGiá vé: " + str(price)+".000" +"\nTài khoản để đăng nhập để kiểm tra vé là: Tên đăng nhập: " + phoneUser +" " + "Mật khẩu: "+ password;
            send_mail('Welcome!', data, "PLC", [email], fail_silently=False)
            print("done")
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
        seat_id2 = data.seat_id
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
        seat1 = "SELECT * FROM managers_seat WHERE id = " + str(seat_id);
        _Seat1 = Seat.objects.raw(seat1)
        for data in _Seat1:
            number_chair=data.number_chair

        seat2 = "SELECT * FROM managers_seat WHERE id = " + str(seat_id2);
        _Seat2 = Seat.objects.raw(seat2)
        for data in _Seat2:
            number_chair2=data.number_chair
        print(number_chair1)
        print(number_chair2)

        number_Seats = "SELECT 1 as id,count(*) as nb_seats FROM managers_ticket WHERE managers_ticket.trip_id = " + str(trip_id) + " group by trip_id";
        number_Seatss = Seat.objects.raw(number_Seats)
        for data in number_Seatss:
              number_Seat=data.nb_seats
        request.session['departure'] = departure
        request.session['destination'] = destination
        request.session['departure_time'] = str(departure_time)
        request.session['price'] = price
        request.session['fullnameGarage'] = fullnameGarage
        request.session['description'] = description
        request.session['number_chair'] = number_chair
        request.session['number_chair2'] = number_chair2
        request.session['number_Seat'] = str(number_Seat)
        # request.session['status'] = status
        
def quanlyveInfo(request):
   content = {}
   if 'departure' in request.session:
        if (request.session['departure']):
            departure = request.session['departure']
            content['departure'] = departure
   if 'destination' in request.session:
        if (request.session['destination']):
            destination = request.session['destination']
            content['destination'] = destination
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
   if 'number_chair2' in request.session:
        if (request.session['number_chair2']):
            number_chair2 = request.session['number_chair2']
            content['number_chair2'] = number_chair2
   if 'number_Seat' in request.session:
        if (request.session['number_Seat']):
            number_Seat = request.session['number_Seat']
            content['number_Seat'] = number_Seat
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
