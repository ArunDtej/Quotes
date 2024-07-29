from django.contrib import admin
from django.urls import path
from .views import userLogin, userSignup, userLogout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', userLogin, name = 'userLogin'),
    path('signup/', userSignup, name = 'userSignup'),
    path('logout/', userLogout, name = 'userLogout')

]
