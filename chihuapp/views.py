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

        userType = userAccount.type
        print userType
        if userType == chihu_pb2.CUSTOMER:
            permission = Permission.objects.get(content_type=content_type,codename='customer')
        else:
            permission = Permission.objects.get(content_type=content_type,codename='provider')
        
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

        body = request.body
        loginRequest = chihu_pb2.LoginRequest()
        loginRequest.ParseFromString(body)
        user = authenticate(username=loginRequest.username,password=loginRequest.password)
        if user is not None:
            print("user is not None")

            login(request,user)

            resp = chihu_pb2.LoginResponse()
            resp.status = chihu_pb2.succeed

            print user.get_all_permissions()
            if user.has_perm('chihuapp.customer'):
                resp.type = chihu_pb2.CUSTOMER
                print "customer"
            else:
                resp.type = chihu_pb2.PROVIDER
                print "provider"

            pbstr = resp.SerializeToString()
            return HttpResponse(pbstr)
        else:
            print("user is None")
            resp = chihu_pb2.LoginResponse()
            resp.status = chihu_pb2.fail
            resp.message = u'登陆失败'
            resp.type = chihu_pb2.CUSTOMER

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

        canteenId = viewMealsRequest.canteenId
        
        viewMealsResponse = chihu_pb2.ViewMealsResponse()

        dishes = Dish.objects.filter(canteen_id=canteenId)

        for dish in dishes:
            meal_pb = chihu_pb2.Meal()
            meal_pb.name = dish.name
            # meal_pb.price = dish.price
            price = dish.price
            meal_pb.price = str(dish.price)
            meal_pb.imageUrl=''
            viewMealsResponse.meals.extend([meal_pb])

        pbstr = viewMealsResponse.SerializeToString()
        return HttpResponse(pbstr,content_type="text/plain")
    return HttpResponse("error")

def updateProfile(request):
    if request.method == 'POST':
        body = request.body
        profile = chihu_pb2.Profile()
        try:
            profile.ParseFromString(body)
        except:
            return HttpResponse("error")
        
        print request.user
        user = User.objects.get(username=request.user.username)
        user.email = profile.email
        userProfile = user.userprofile
        userProfile.phone = profile.phone
        userProfile.receiver = profile.receiver
        userProfile.address = profile.address
        userProfile.save()
        user.save()

        resp = chihu_pb2.Response()
        resp.status = chihu_pb2.succeed
        resp.message = u'修改成功'
        pbstr = resp.SerializeToString()
        return HttpResponse(pbstr)

    return HttpResponse("error")

def getProfile(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        profile = chihu_pb2.Profile()
        profile.username = request.user.username
        profile.email = user.email
        if user.userprofile.netid is not None:
            profile.netid = user.userprofile.netid
        if user.userprofile.phone is not None:
            profile.phone = user.userprofile.phone
        if user.userprofile.receiver is not None:
            profile.receiver = user.userprofile.receiver
        if user.userprofile.address is not None:
            profile.address = user.userprofile.address

        if user.has_perm('chihuapp.customer'):
            profile.type = chihu_pb2.CUSTOMER
        else :
            profile.type = chihu_pb2.PROVIDER

        pbstr = profile.SerializeToString()

        return HttpResponse(pbstr,content_type="text/plain")

    return HttpResponse("error")

def getCanteens(request):
    if request.method=="POST":
        user = User.objects.get(username=request.user.username)
        canteens = Canteen.objects.filter(user=user)

        viewCanteensResponse = chihu_pb2.ViewCanteensResponse()
        for canteen in canteens:
            canteen_pb = chihu_pb2.Canteen()
            canteen_pb.name = canteen.name
            canteen_pb.canteenId = canteen.id
            viewCanteensResponse.canteens.extend([canteen_pb]) 
        pbstr = viewCanteensResponse.SerializeToString()
        return HttpResponse(pbstr,content_type="text/plain")

    else:
        return HttpResponse("error")

def addDish(request):
    if request.method=="POST":
        user = User.objects.get(username=request.user.username)

        addDishRequest = chihu_pb2.AddDishRequest()
        try:
            addDishRequest.ParseFromString(request.body)
        except:
            return HttpResponse("error")

        canteenId = addDishRequest.canteenId
        name = addDishRequest.name
        price = addDishRequest.price

        canteen = Canteen.objects.get(id=canteenId)
        dish1 = Dish(name=name,price=price,canteen=canteen)
        dish1.save()
        print name
        resp = chihu_pb2.Response()
        resp.status = chihu_pb2.succeed
        return HttpResponse(resp.SerializeToString())

    else:
        return HttpResponse("error")

def addCanteen(request):
    if request.method=="POST":
        user = User.objects.get(username=request.user.username)
        addCanteenRequest = chihu_pb2.AddCanteenRequest()
        try:
            addCanteenRequest.ParseFromString(request.body)
        except:
            return HttpResponse("error")
        name = addCanteenRequest.name
        canteen1 = Canteen(user=user,name=name)
        canteen1.save()
        print name
        resp = chihu_pb2.Response()
        resp.status = chihu_pb2.succeed
        return HttpResponse(resp.SerializeToString())
    else:
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