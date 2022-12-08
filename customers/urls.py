from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.index, name='index'),
    path('check/', views.checkCustomer, name='check'),
    path('forgotPassword', views.forgotPassword, name='forgotPassword'),
    path('userInfo', views.userInfo, name='userInfo'),
    path('listCoach', views.listCoach, name='listCoach'),
    path('datve', views.datve, name='datve'),
    path('_login', views.loginView, name='login'),
     path('quanlyve', views.quanlyveView, name='login'),

]