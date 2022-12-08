from django.urls import path
from . import views

app_name = 'managers'

urlpatterns = [
    #Manager
    path('', views.index, name='index'),
    path('/login', views.managerLogin, name='managerLogin'),
    path('/login/loginrecord/', views.managerLoginRecord, name='managerLoginRecord'),
    path('/signup', views.managerSignup,name='managerSignup'),
    path('/signup/record/', views.managerSignUpRecord,name='managerSignupRecord'),
    path('/profile/edit/', views.editProfile,name='editProfile'),
    path('/profile/edit/record/', views.editProfileRecord, name='editProfileRecord'),
    path('/profile/editPass/', views.editPassword, name='editPassword'),
    path('/profile/editPass/record/', views.editPasswordRecord, name='editPasswordRecord'),

    #Trip
    path('/add/', views.addtrip, name='addtrip'),
    path('/add/addtrip/', views.addrecordtrip, name='addrecordtrip'),
    path('/view/trip/<int:id>',views.viewTrip, name='viewTrip'),
    path('/edit/trip/<int:id>', views.edittrip, name='edittrip'),
    path('/edit/edittrip/<int:id>', views.editrecordtrip, name='editrecordtrip'),
    path('/delete/trip/<int:id>', views.deletetrip, name='deletetrip'),

    #Garage
    path('/edit/garage/', views.editGarage, name='editGarage'),
    path('/edit/garage/record/', views.editGarageRecord, name='editGarageRecord'),

    #Seat
    path('/view/seat/<int:id>',views.viewSeat,name='viewSeat'),

    #Schedule
    path('/add/schedule/', views.addSchedule, name='addSchedule'),
    path('/add/schedule/record/',views.addScheduleRecord, name='addScheduleRecord'),
    path('/delete/schedule/<int:id>', views.deleteSchedule, name='deleteSchedule'),

    #Revenue
    path('/revenue',views.managerRevenue, name='managerRevenue'),
]