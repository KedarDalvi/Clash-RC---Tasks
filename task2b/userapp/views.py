from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from userapp.models import UserProfile

def page1(request):
    if request.method == 'GET':
        return render(request, 'page1.html')
    elif request.method == 'POST':
        username = request.POST.get('user')
        email = request.POST.get('email')
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        phone = request.POST.get('phone')
        password = request.POST.get('f_pass')
        password2 = request.POST.get('c_pass')
        if (password == password2):
            try:
                profile = User.objects.get(username = username)
                return render(request, 'page1.html', {"message":"Username already exists."})
            except User.DoesNotExist:
                user = User.objects.create_user(username = username, email = email, first_name = first_name, last_name = last_name, password = password)
                user.save()
                profile = UserProfile(username = username, ph_no = phone)
                UserProfile.save()
                return render(request, 'page1.html', {"message":"User has been registered."})
        else:
            return render(request, 'page1.html', {"message":"Passwords don't match."})

def login(request):
    if request.method == 'GET':
        return render(request, 'page2.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'page3.html', {"message":"User logged in successfully!"})
        else:
            return render(request, 'page2.html', {"message":"Invalid Credentials. Try Again."})

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return render(request, 'page3.html')

def signup_again(request):
    return render(request, 'page1.html', {'message':"Logged Out Successfully!"})



















