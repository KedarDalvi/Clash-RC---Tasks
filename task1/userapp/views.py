from django.shortcuts import render

def home(request):
    if request.method == 'GET':
        a = [ i for i in range (1,21)]
        context = {'numbers' : a}
        return render(request, 'home.html', context)

    if request.method == 'POST':
        start = request.POST.get('number1')
        end = request.POST.get('number2')
        start = int(start)
        end = int(end)
        b = [i for i in range (start, end + 1)]
        context1 = {'numbers' : b}
        return render(request, 'result.html', context1)