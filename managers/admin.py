from django.contrib import admin
from managers.models import Manager
from managers.models import Garage
from managers.models import Trip
from managers.models import Seat
from managers.models import Schedule

# Register your models here.
class ManagerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fullName',
        'phoneNumber',
        'email',
        'password'
        )
    list_display_links = (
        'id',
        'fullName',
        'phoneNumber',
        'email',
        'password'
        )
    list_per_page = 5
    sortable_by = ('id')
    # list_filter = ('fullName', )
admin.site.register(Manager, ManagerAdmin)

class GarageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fullName',
        'description'
        )
    list_display_links = (
        'id',
        'fullName',
        'description'
        )
    list_per_page = 5
    sortable_by = ('id')
    # list_filter = ('fullName', )
admin.site.register(Garage, GarageAdmin)

# Test manager
admin.site.register(Trip)
admin.site.register(Seat)
admin.site.register(Schedule)