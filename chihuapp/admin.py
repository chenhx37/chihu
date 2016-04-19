from django.contrib import admin
from models import *
# Register your models here.

admin.site.register(UserPermission)
admin.site.register(TimePeriod)
admin.site.register(Canteen)
admin.site.register(Dish)
admin.site.register(DishAndNumberPair)
admin.site.register(Order)
admin.site.register(UserProfile)