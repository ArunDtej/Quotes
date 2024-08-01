from django.shortcuts import render, HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import NameForm
from .models import FriendsList, Notification, Posts, Comments
from django.contrib.auth.models import User
from django.contrib import messages

@login_required(login_url= '/auth/login/')
def home(request):
    #home page to display posts from friends with paging
    print('User: {}'.format(request.user))
    return render(request, 'home.html', {'name': request.user.get_full_name()})

@login_required(login_url= '/auth/login/')
def friendsPage(request):
    #fetch and display friends
    user = User.objects.filter(email = request.user.email).first()
    print(request.user.email)
    fl = FriendsList.objects.filter(user = user).first()
    if not fl:
        raise Http404("User not found")
    return render(request, 'friendspage.html',  {'name': request.user.get_full_name(), 'friends': fl.friends.all()})

@login_required(login_url= '/auth/login/')
def Notif(request):
    #fetch and display notifications
    notification = Notification.objects.filter(user= request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'name': request.user.get_full_name(), 'notification': notification})

@login_required(login_url= '/auth/login/')
def acceptFriendRequest(request, notif_id):
    # accepts friend request from notifications
    notification = Notification.objects.get(id = notif_id)
    if not notification:
        raise Http404("Notification not found")
    
    user = User.objects.filter(email = request.user.email).first()
    fl = FriendsList.objects.filter(user = user).first()
    if not fl:
        raise Http404("User not found")
    fl.accept_request(User.objects.filter(username=notification.from_user).first())
    notification.delete()
    messages.success(request, "Login Successful")
    return Notif(request)

@login_required(login_url= '/auth/login/')
def clearNotifications(request):
    #clears all notifications
    user = User.objects.filter(email = request.user.email).first()
    fl = FriendsList.objects.filter(user = user).first()
    if not fl:
        raise Http404("User not found")
    Notification.objects.filter(user=request.user).delete()
    return Notif(request)

@login_required(login_url= '/auth/login/')
def deleteNotification(request, notif_id):
    #deletes individual notification
    notification = Notification.objects.get(id = notif_id)
    if not notification:
        raise Http404("Notification not found")
    notification.delete()
    return Notif(request)

@login_required(login_url='/auth/login/')
def unFriend(request, user_id):
    #removes friend from friends page
    friend = User.objects.filter(id = user_id).first()
    user = User.objects.filter(email = request.user.email).first()
    FriendsList.objects.filter(user = user).first().unfriend(friend)
    return friendsPage(request)

   

@login_required(login_url= '/auth/login/')
def Profile(request, user_id = None):
    if user_id == None or user_id == request.user.id:
        user = User.objects.filter(email = request.user.email).first()
        posts = Posts.objects.filter(user = user).all().order_by('-created_at')

        context = {"name": request.user.get_full_name(), 
        "username": request.user.username, 
        "email": request.user.email,
        "posts": posts,
        "friends": FriendsList.objects.filter(user = user).first().friends.all()
        }
        return render(request, 'my_profile.html', context)
    else:
        user = User.objects.filter(id = user_id).first()
        return render(request, 'profile_template.html', {'name': request.user, "friend" : user.get_full_name()})

@login_required(login_url= '/auth/login/')  
def uploadPost(request):
    content = request.POST.get('postContent', '')
    print(content)
    post = Posts.objects.create(user=request.user, content=content)
    post.save()
    return Profile(request, request.user.id)