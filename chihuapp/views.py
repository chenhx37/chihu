# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User,Permission
from django.contrib.auth import authenticate, login
from chihuapp.models import *
from django.contrib.contenttypes.models import ContentType
from CHIHU_PROTOCOL import chihu_pb2
import json
import traceback
from django.contrib.auth.decorators import login_required
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

        if User.objects.filter(username=uname).exists():
            resp = chihu_pb2.Response()
            resp.status = chihu_pb2.fail
            resp.message = u'用户名已存在'
            pbstr = resp.SerializeToString()

            return HttpResponse(pbstr)
        
        user = User.objects.create_user(uname,email,password)
        content_type = ContentType.objects.get_for_model(UserPermission)

        permission = Permission.objects.get(content_type=content_type,codename='customer')
        user.user_permissions.add(permission)
        UserProfile.objects.get_or_create(user=user)

        resp = chihu_pb2.Response()
        resp.status = chihu_pb2.succeed
        resp.message = u'创建用户成功'

        pbstr = resp.SerializeToString()
        return HttpResponse(pbstr)

    return HttpResponse("error")

def loginUser(request):
    if request.method == "POST":

        print request.COOKIES

        body = request.body
        loginRequest = chihu_pb2.LoginRequest()
        loginRequest.ParseFromString(body)
        user = authenticate(username=loginRequest.username,password=loginRequest.password)
        if user is not None:
            print("user is not None")

            login(request,user)

            resp = chihu_pb2.Response()
            resp.status = chihu_pb2.succeed
            resp.message = u'登陆成功'

            pbstr = resp.SerializeToString()
            return HttpResponse(pbstr)
        else:
            print("user is None")
            resp = chihu_pb2.Response()
            resp.status = chihu_pb2.fail
            resp.message = u'登陆失败'
            pbstr = resp.SerializeToString()
            return HttpResponse(pbstr)

    return HttpResponse("error")

def viewCanteens(request):
    if request.method == 'POST':
        body = request.body
        viewCanteensRequest = chihu_pb2.ViewCanteensRequest()
        try:
            viewCanteensRequest.ParseFromString(body)
        except:
            return HttpResponse("error")

        viewCanteensResponse = chihu_pb2.ViewCanteensResponse()

        canteens = Canteen.objects.all()
        for canteen in canteens:
            canteen_pb = chihu_pb2.Canteen()
            canteen_pb.name = canteen.name
            canteen_pb.canteenId = canteen.id
            viewCanteensResponse.canteens.extend([canteen_pb]) 

        pbstr = viewCanteensResponse.SerializeToString()
        return HttpResponse(pbstr)
    return HttpResponse("error")

def viewMeals(request):
    if request.method == 'POST':
        body = request.body
        viewMealsRequest = chihu_pb2.ViewMealsRequest()
        try:
            viewMealsRequest.ParseFromString(body)
        except:
            return HttpResponse("error")

        print("hello1")

        canteenId = viewMealsRequest.canteenId
        print("hello2")
        print(canteenId)
        viewMealsResponse = chihu_pb2.ViewMealsResponse()
        print("hello3")
        dishes = Dish.objects.filter(canteen_id=canteenId)
        print("hello4")
        for dish in dishes:
            meal_pb = chihu_pb2.Meal()
            meal_pb.name = dish.name
            # meal_pb.price = dish.price
            price = dish.price
            meal_pb.price = str(dish.price)
            print meal_pb.price
            meal_pb.imageUrl=''
            viewMealsResponse.meals.extend([meal_pb])

        pbstr = viewMealsResponse.SerializeToString()
        return HttpResponse(pbstr,content_type="text/plain")
    print("hell")
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