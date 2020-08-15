from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from userapp.models import UserProfile


def page1(request):
    if request.method == 'GET':
        return render(request, 'page1.html')
    elif request.method == 'POST':
        use_name = request.POST.get('user')
        email = request.POST.get('email')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        ph_no = request.POST.get('ph_no')
        f_pass = request.POST.get('f_pass')
        c_pass = request.POST.get('c_pass')




