#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.models import User
from coffee.models import Product
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    allproducts = Product.objects.all()
    return render(request, 'home.html',{'allproducts': allproducts})


def register(request):
    if request.method == "POST":
        username = request.POST.get('user_name')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        if pwd != cpwd:
            return render(request, 'user_register.html', {'errmsg': 'password not same'})
        try:
            temp = User.objects.get(username=username)
        except Exception as e:
            temp = None
        if temp:
            return render(request, 'user_register.html', {'errmsg': 'user exist'})

        user = User.objects.create_user(username=username,password=pwd,email=email)
        user.is_active = 1
        user.save()
        return render(request, 'user_login.html', {'errmsg': 'Register Successful, Please login'})
    return render(request, 'user_register.html')


def login(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')

    if request.method == "POST":
        username = request.POST.get('user')
        pwd = request.POST.get('pwd')
        user = auth.authenticate(username=username,password=pwd)
        if user:
            auth.login(request, user)
            return redirect("/group6coffee/productlist", {'user_name': username})

    return render(request, 'user_login.html')


def logout(request):
    auth.logout(request)
    return redirect('/group6coffee/index')


def productlist(request):

    if not request.user.is_authenticated:
        return render(request, 'user_login.html')
    else:
        allproducts = Product.objects.all()
        return render(request, 'productlist.html', {'user_name': request.user,'allproducts': allproducts})


@csrf_exempt
def handleorder(request):
    if request.method == "POST":
        print('yes')
        print(request.body)
    return HttpResponse("try fetch", status=200)
