from django.contrib import admin
from customers.models import Customer

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
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
admin.site.register(Customer, CustomerAdmin)