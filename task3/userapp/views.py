from django.shortcuts import render
from django.contrib.auth.models import User, auth
from userapp.models import UserProfile, Question, Response
import re

def signup(request):
    if request.method == 'GET':
        return render(request, 'SignUp.html')
    else:
        username = request.POST.get('username')
        regex = '^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)$'
        if (re.search(regex, username) == None) :
            return render(request, 'SignUp.html', {'message':'Enter a Valid Username.'})
        else:
            first_name = request.POST.get('first_name')
            if (first_name.isalpha() == False):
                return render(request, 'SignUp.html', {'message':'Enter Correct First Name'})
            else:
                last_name = request.POST.get('last_name')
                if (last_name.isalpha() == False):
                    return render(request, 'SignUp.html', {'message':'Enter Correct Last Name.'})
                else:
                    email = request.POST.get('email')
                    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                    if (re.search(regex, email) == None):
                        return render(request, 'SignUp.html', {'message':'Enter valid Email address.'})
                    else:
                        phone = request.POST.get('phone')
                        if ((phone.isdigit() == False) | (len(str(phone)) != 10) | ( (str(phone)[0] in ['0','1','2','3','4','5']) == True)):
                            return render(request, 'SignUp.html', {'message':'Enter a valid Phone number.'})
                        else:
                            f_pass = request.POST.get('f_pass')
                            if ((len(str(f_pass)) < 8) ):
                                return render(request, 'SignUp.html', {'message':'Enter a strong Password.'})
                            else:
                                if ((len(str(f_pass)) > 32)):
                                    return render(request, 'SignUp.html', {'message':'Password too long.'})
                                else:
                                    if not any(char.isdigit() for char in f_pass):
                                        return render(request, 'SignUp.html', {'message':"Password doesn't contain digits."})
                                    else:
                                        if not any(char.isupper() for char in f_pass):
                                            return render(request, 'SignUp.html', {'message':"Password doesn't contain any Uppercase character."})
                                        else:
                                            if not any(char.islower() for char in f_pass):
                                                return render(request, 'SignUp.html', {'message':"Password doesn't contain any Lowercase character."})
                                            else:
                                                special = ['!','#','%','&','*','+','-','.','/',';',':','<','=','>','?','@','~','{','}','(',')','|','^','`','[',']','_',' ',"'",'"']
                                                if not any(char in special for char in f_pass):
                                                    return render(request, 'SignUp.html', {'message':"Password doesn't contain any special characters."})
                                                else:
                                                    c_pass = request.POST.get('c_pass')
                                                    if c_pass == f_pass:
                                                        try:
                                                            user = User.objects.get(username = username)
                                                            return render(request, 'SignUp.html', {'message':'Username already exists.'})
                                                        except User.DoesNotExist:
                                                            user = User.objects.create_user(username = username, first_name = first_name, last_name = last_name, email = email, password = f_pass)
                                                            profile = UserProfile(user = user, phone = phone)
                                                            profile.save()
                                                            return render(request, 'SignUp.html', {'message':'User Registered Successfully.'})
                                                    return render(request, 'SignUp.html', {'message':"Passwords don't match"})

def signin(request):
    if request.method == 'GET':
        return render(request, 'SignIn.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username = username, password = password)
        if user is not None :
            auth.login(request, user)
            return render(request, 'home.html', {'message': user})
        else:
            return render(request, 'SignIn.html', {'message':'Invalid Credentials.'})

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return render(request, 'SignIn.html', {'message':'You logged out Successfully.'})


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
