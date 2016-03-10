# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User,Permission
from chihuapp.models import *
from django.contrib.contenttypes.models import ContentType
from CHIHU_PROTOCOL import chihu_pb2

# Create your views here.

def index(request):
    return HttpResponse("what?index!")

def registerCustomer(request):
    # return HttpResponse("hello")
    if request.method == "POST":
        body = request.body
        userAccount = chihu_pb2.UserAccount()
        userAccount = userAccount.FromString(body)

        uname = userAccount.username
        password=userAccount.password
        email=userAccount.email
        school=userAccount.school

        # return HttpResponse(uname+" "+password+" "+email)

        if User.objects.filter(username=uname).exists():
            resp = chihu_pb2.Response()
            resp.status = chihu_pb2.fail
            resp.message = "用户名已存在"
            return HttpResponse(resp.SerializeToString())
        
        user = User.objects.create_user(uname)
        user.set_password(password)
        user.set_email(email)        
        content_type = ContentType.objects.get_for_model(UserPermission)
        permission = Permission.objects.get(content_type=content_type,codename='customer')
        user.user_permissions.add(permission)
        user.save()

        if UserProfile.objects.filter(user=user).exists():
            resp = chihu_pb2.Response()
            resp.status = chihu_pb2.fail
            resp.message = "无法创建用户"
            return HttpResponse(resp.SerializeToString())

        userProfile = UserProfile.objects.create(user=user,school='SunYatSanUniversity')
        userProfile.save()

        resp = chihu_pb2.Response()
        resp.status = chihu_pb2.succeed
        resp.message = '创建用户成功'

        return HttpResponse(resp.SerializeToString)

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