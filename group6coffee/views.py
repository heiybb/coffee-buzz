#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.models import User
from coffee.models import Product
from coffee.models import OrderItem
from coffee.models import Order
from coffee.models import Paymentstatus
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import datetime


def index(request):
    allproducts = Product.objects.all()
    if request.user.is_authenticated:
        return render(request, 'home_login.html',{'allproducts': allproducts,'user_name':request.user})
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
        return render(request, 'home_login.html')

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
        showorderinfo = ''
        if Paymentstatus.objects.filter(ordercontent='N'):
            showorderinfo = ''
        else:
            pay = Paymentstatus.objects.all()
            for i in pay:
                showorderinfo = i.ordercontent + ', order complete.'
                i.ordercontent = 'N'
                i.save()

        return render(request, 'productlist.html',
                      {'user_name': request.user,'allproducts': allproducts,'showorderinfo':showorderinfo})


def orderlist(request):
    if not request.user.is_authenticated:
        return render(request, 'user_login.html')
    else:
        orders = OrderItem.objects.filter(user_name=request.user).order_by('-created_at')
        return render(request, 'orderlist.html',{'user_name': request.user,'orders':orders})


def queuelist(request):
    if not request.user.is_authenticated:
        return render(request, 'user_login.html')
    else:
        # orders = OrderItem.objects.get_queryset().order_by('-article_id')
        orders = OrderItem.objects.all();
        return render(request, 'queuelist.html',{'user_name': request.user,'orders':orders})



def getproductinfo(id):
    info = []
    id = int(id)
    product = Product.objects.get(product_id=id)
    info.append(product.product_name)
    info.append(product.product_price)
    info.append(product.product_type)
    return info


def updateproductquantity(id, no):
    id = int(id)
    product = Product.objects.get(product_id=id)
    product.product_quantity = product.product_quantity - no
    product.save()


@csrf_exempt
def handleorder(request):
    if request.method == "POST":
        # receive msg like, product_id:quantity
        # update
        isValid = False
        tt = request.body
        order = json.loads(tt)
        user_name = ''
        for item in order:
            if item == 'user_name':
                user_name = order[item]

        content = 'Hi, ' + user_name + ","
        for i in order:
            if i == 'user_name':
                continue
            else:
                print(user_name)
                temp = getproductinfo(i)
                product_name = temp[0]
                product_price = temp[1]
                product_type = temp[2]
                order_status = 'Receive'
                order_number = int(order[i])
                order_sub_total = product_price * order_number
                oi = OrderItem(product_name=product_name,product_price=product_price,order_status=order_status,
                               order_number=order_number,order_sub_total=order_sub_total,user_name=user_name)
                oi.save()
                # print(oi.order_item_id)
                # orderid = oi.order_item_id
                # order_list = Order(order_item_id=orderid)
                # order_list.save()

                content = content + product_name + " "
                isValid = True

                ##update cake and sandwiches menu
                if product_type == "Cake":
                    updateproductquantity(i,order_number)
                if product_type == 'Sandwiches':
                    updateproductquantity(i, order_number)

        if isValid:
            isValid = False
            pay = Paymentstatus.objects.all()
            for i in pay:
                i.ordercontent=content
                i.save()

        return HttpResponse(status=200)


def deleteOrder(order_item_id):
    order_item_id = int(order_item_id)
    oi = OrderItem.objects.get(order_item_id=order_item_id)
    oi.delete()

    print('test')
    # oo = Order.objects.get(order_item_id=order_item_id)
    # oo.delete()


@csrf_exempt
def cancelorder(request):
    if request.method == "POST":
        tt = request.body
        order = json.loads(tt)
        user_name = ''
        order_item_id = ''
        is_valid = False

        print(order)

        for item in order:
            # if item == 'user_name':
            #     user_name = order[item]
            #     print(order[item])
            if item == 'order_item_id':
                order_item_id = order[item]
                print(order[item])
                is_valid = True

        if is_valid:
            deleteOrder(order_item_id)

        return HttpResponse(status=200)


