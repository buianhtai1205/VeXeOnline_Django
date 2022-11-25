from django.contrib import admin
from managers.models import Manager
from managers.models import Garage

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
        'desciption'
        )
    list_display_links = (
        'id',
        'fullName',
        'desciption'
        )
    list_per_page = 5
    sortable_by = ('id')
    # list_filter = ('fullName', )
admin.site.register(Garage, GarageAdmin)