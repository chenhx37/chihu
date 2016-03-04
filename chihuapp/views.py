# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User,Permission
from chihuapp.models import *
from django.contrib.contenttypes.models import ContentType
from CHIHU_PROTOCOL import CHIHU_pb2

# Create your views here.

def index(request):
    return HttpResponse("what?index!")

def registerCustomer(request):
    if request.method == "POST":
        body = request.body
        userAccount = CHIHU_pb2.UserAccount()
        userAccount = userAccount.FromString(body)

        uname = userAccount.username
        password=userAccount.password
        email=userAccount.email
    
        return HttpResponse(username+" "+password+" "+email)

        # if User.objects.filter(username=uname).exists():
        #     return HttpResponse("username already used!")
        
        # user = User.objects.create_user(uname)
        
        # password = userAccount.password
        # user.set_password(password)

        # email = userAccount.email
        


        # content_type = ContentType.objects.get_for_model(UserPermission)
        # permission = Permission.objects.get(content_type=content_type,codename='customer')
        
        # user.user_permissions.add(permission)
        # user.save()

        # return HttpResponse("register,"+user.get_username())

    return HttpResponse("error")

def pbtest(request):
    ua = CHIHU_pb2.UserAccount()
    ua.username='chen'
    ua.password='chen'
    ua.email='465462686@qq.com'
    out = ua.SerializeToString()
    print("SerializeToString ok")

    ua1 = CHIHU_pb2.UserAccount()
    ua1 = ua1.FromString(out)
    print ua1.username,ua.password,ua.email
    return HttpResponse("test")