from django.contrib import admin

from .models import *

admin.site.register(Receipt)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Promotion)
admin.site.register(Address)