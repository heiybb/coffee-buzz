from django.urls import path, include
import group6coffee.views

urlpatterns = [
    path('index', group6coffee.views.index),
    path('register', group6coffee.views.register),
    path('login', group6coffee.views.login),
    path('productlist',group6coffee.views.productlist),
    path('logout',group6coffee.views.logout),
    path('orderlist',group6coffee.views.orderlist),
    path('handleorder',group6coffee.views.handleorder),
    path('cancelorder',group6coffee.views.cancelorder),
    path('queuelist',group6coffee.views.queuelist)
]