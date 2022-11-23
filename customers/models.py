from django.db import models

# Create your models here.
class Customer(models.Model):
    fullName = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=200)

    def __unicode__(self):
        return self.content
    