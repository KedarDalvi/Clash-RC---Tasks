from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', page1, name = 'page1'),
    path('page2/', login, name = 'page2'),
    path('page3/',logout, name = 'page3'),
    path('signup_page/', signup_again, name = 'signup_again')
]