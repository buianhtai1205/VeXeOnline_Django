from django.db import models
from customers.models import Customer

# Create your models here.

class Garage(models.Model):
    fullName = models.CharField(max_length=50)
    desciption = models.CharField(max_length=200)
    deleted = models.IntegerField(default=0)

    def __unicode__(self):
        return self.content
class Manager(models.Model):
    fullName = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    garage_id = models.ForeignKey(Garage, on_delete=models.CASCADE, verbose_name="Garage", default=None)

    def __unicode__(self):
        return self.content

class Schedule(models.Model):
    musty = models.CharField(max_length=100)
    status = models.IntegerField
    garage_id = models.ForeignKey(Garage, on_delete=models.CASCADE, verbose_name="Garage")

    def __unicode__(self):
        return self.content

class Trip(models.Model):
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    price = models.IntegerField()
    num_seat = models.IntegerField(default=0)
    garage_id = models.ForeignKey(Garage, on_delete=models.CASCADE, verbose_name="Garage")

    def __unicode__(self):
        return self.content
    

class Seat(models.Model):
    number_chair = models.CharField(max_length=20)
    status = models.CharField(max_length=50, default=0)
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name="Trip")

    def __unicode__(self):
        return self.content
    

class Ticket(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE, verbose_name="Trip")
    seat_id = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name="Seat")
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name="Schedule", null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['trip_id', 'seat_id', 'customer_id'], name='unique_trip_seat_customer_combination'
            )
        ]

    def __unicode__(self):
        return self.content
    