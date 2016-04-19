# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

# Create your models here.
class UserPermission(models.Model):
    class Meta:
        permissions = (("customer","can use customer version"),
            ("provider","can use provider version"),)


######################################
class TimePeriod(models.Model):
    Canteen = models.ForeignKey("Canteen")
    start_time = models.TimeField()
    end_Time = models.TimeField()
######################################

class Canteen(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30,null=True)

class Dish(models.Model):
    canteen = models.ForeignKey(Canteen,default=None)
    name = models.CharField(max_length=30)
    price = models.FloatField()
    picture = models.FileField(upload_to='./dish_img',null=True,default=None)            #可能需要用FileField
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    score = models.FloatField(default=0)

class DishAndNumberPair(models.Model):
    dish = models.ForeignKey(Dish)
    number = models.PositiveSmallIntegerField()

class Order(models.Model):
    FINISHED = 0
    UNSCORED = 1
    CANCELED = 2
    DELIVERING = 3
    STATUS_CHOICES = (
        (FINISHED,'Finished'),
        (UNSCORED,'Unscored'),
        (CANCELED,'Canceled'),
        (DELIVERING,'Delivering')
    )
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    dish_list = models.ManyToManyField(DishAndNumberPair)
    total_price = models.FloatField()
    receiver = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    customer = models.ForeignKey(User,related_name="customer")
    provider = models.ForeignKey(User,null=True,related_name="provider")
    @staticmethod
    def count_total_price(instance,**kwargs):
        if kwargs['action'] == 'post_add':
            if instance.total_price == 0.0:
                inctance = Order.objects.get(id=instance.id)
                for dish in instance.dish_list.all():
                    instance.total_price += dish.price
            if instance.total_price > 0:
                instance.save()
    
m2m_changed.connect(Order.count_total_price,sender=Order.dish_list.through)


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    netid = models.CharField(max_length=30,null=True)
    phone = models.CharField(max_length=20,null=True)
    receiver = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=50,null=True)
    SUN_YAT_SAN_UNIVERSITY = 0
    # SCHOOL_CHOICES = (
    #     (SUN_YAT_SAN_UNIVERSITY,'SunYatSanUniversity'),
    # )
    # school = models.PositiveSmallIntegerField(choices=SCHOOL_CHOICES)

# class Contact(models.Model):
#     user = models.ForeignKey(UserProfile)
#     address = models.CharField(max_length=50)
#     phone_number = models.CharField(max_length=20)