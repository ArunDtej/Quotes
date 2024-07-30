from django.shortcuts import render, HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import NameForm
from .models import FriendsList, Notification
from django.contrib.auth.models import User

@login_required(login_url= '/auth/login/')
def home(request):
    print('User: {}'.format(request.user))
    return render(request, 'home.html', {'name': request.user})

@login_required(login_url= '/auth/login/')
def friendsPage(request):
    user = User.objects.filter(email = request.user.email).first()
    print(request.user.email)
    fl = FriendsList.objects.filter(user = user).first()
    if not fl:
        raise Http404("User not found")
    return render(request, 'friendspage.html',  {'name': request.user, 'friends': fl.friends.all()})

@login_required(login_url= '/auth/login/')
def Notif(request):
    notification = Notification.objects.filter(user= request.user)
    return render(request, 'notifications.html', {'name': request.user, 'notification': notification})


def makeform(request):
    if request.method =='POST':
        myform = NameForm(request.POST)
        if myform.is_valid():
            pass
        return HttpResponse(f'{myform.cleaned_data['address']}, {myform.cleaned_data['your_name']}')
    else:
        myform = NameForm()
    return render(request,'myform.html', {'form': myform})