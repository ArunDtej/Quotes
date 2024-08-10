from django.shortcuts import render, HttpResponse
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import NameForm
from .models import FriendsList, Notification, Posts, Comments
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse

def home(request):
    user = request.user

    now = timezone.now()
    two_days_ago = now - timedelta(days=2)

    friends_list = FriendsList.objects.get(user=user)
    friends = friends_list.friends.all()

    posts = Posts.objects.filter(user__in=friends, created_at__gte=two_days_ago).order_by('-created_at')


    return render(request, 'home.html', {'posts': posts, 'name': request.user.get_full_name()})


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
def search_user(request):
    email = request.GET.get('email', '').strip()
    print(email)
    if email:
        user = User.objects.filter(email=email).first()
        if user:
            profile_url = reverse('profile_with_id', kwargs={'user_id': user.id})
            return redirect(profile_url)
    return HttpResponse('User not found', status=404)
   

@login_required(login_url= '/auth/login/')
def Profile(request, user_id = None):
    try:
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
            are_friends =  FriendsList.objects.filter(user = request.user).first().are_friends(user)
            
            return render(request, 'profile_template.html', { "friends": FriendsList.objects.filter(user = user).first().friends.all(),
                'name': user.get_full_name(), "username": user.username, "email": user.email, "posts": Posts.objects.filter(user = user).all().order_by('-created_at'), "are_friends": are_friends, "friend_id": user_id})
    except Exception as e:
        return HttpResponse("User not found")

@login_required(login_url= '/auth/login/')  
def uploadPost(request):
    if request.method == 'POST':
        print("in the function")
        content = request.POST.get('postContent')
        post = Posts.objects.create(user=request.user, content=content)
        post.save()
        
    return Profile(request, request.user.id)

@login_required(login_url= '/auth/login/')
def deletePost(request, post_id):
    try:
        post = Posts.objects.filter(id = post_id)[0]
        if post.user != request.user:
            return HttpResponse("You are not authorized to delete this post")
    
        post.delete()
    except Exception as e:
        return HttpResponse("Failed to delete post")

    return HttpResponse("Successfully deleted post")


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import FriendsList, User

@login_required(login_url='/auth/login/')
def send_friend_request(request):
    if request.method == 'POST':
        friend_id = request.POST.get('friend_id')
        friend = get_object_or_404(User, id=friend_id)
        user_friends_list = FriendsList.objects.get(user=request.user)
        user_friends_list.add_friend(friend)
        
        return JsonResponse({'action': 'sent'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='/auth/login/')
def unfriend_user(request):
    if request.method == 'POST':
        friend_id = request.POST.get('friend_id')
        friend = get_object_or_404(User, id=friend_id)
        user_friends_list = FriendsList.objects.get(user=request.user)
        user_friends_list.unfriend(friend)
        
        return JsonResponse({'action': 'removed'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
