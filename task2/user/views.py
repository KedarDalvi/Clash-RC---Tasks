from django.shortcuts import render, redirect
from user.models import UserProfile

def home(request):
    if request.method == 'GET':
        return render(request, 'page1.html')
    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        contact = request.POST.get('contact')
        email_id = request.POST.get('email_id')
        gender = request.POST.get("gender")
        profile = UserProfile(f_name = f_name, l_name = l_name, ph_no = contact, email = email_id, gender = gender)
        profile.save()
        return redirect('home')

def page2(request):
    if request.method == 'POST':
        email_id = request.POST['email']
        try:
            profile = UserProfile.objects.get(email=email_id)
            return render(request, 'page3.html', {'profile':profile, 'message':'User Found !'})
        except UserProfile.DoesNotExist:
            return render(request, 'page3.html', {'message':'Sorry. User not found.'})
    else:
        return render(request, 'page2.html')


