from django.conf.urls import url, include
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from . import views

urlpatterns = [

    path('',views.index,name='index'),
    path('login',views.index,name='login'),
    path('logout',views.logout,name='logout'),
    path('signuppage',views.signuppage,name="signuppage"),
    path('home',views.home,name="home"),
    path('usersignup',views.usersignup,name="usersignup"),
    path('userlogin',views.userlogin,name="userlogin"),
    path('search',views.search,name="search"),
    path('sendmail/<int:id>',views.sendmail,name="sendmail"),
    path('sendmassmail',views.sendmassmail,name="sendmassmail")


]