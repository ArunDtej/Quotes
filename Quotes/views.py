from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import NameForm

@login_required(login_url= '/auth/login/')
def home(request):
    print('User: {}'.format(request.user))
    return render(request, 'home.html', {'name': request.user})

def friendsPage(request):
    return render(request, 'friendspage.html',  {'name': request.user})

def makeform(request):
    if request.method =='POST':
        myform = NameForm(request.POST)
        if myform.is_valid():
            pass
        return HttpResponse(f'{myform.cleaned_data['address']}, {myform.cleaned_data['your_name']}')
    else:
        myform = NameForm()
    return render(request,'myform.html', {'form': myform})