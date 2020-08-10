from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('page2/', page2, name = 'page2'),

]
