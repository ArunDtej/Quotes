
from django.contrib import admin
from django.urls import path, include
from .views import home, friendsPage, Notif, clearNotifications, acceptFriendRequest, deleteNotification, Profile
from .views import unFriend, uploadPost, deletePost, send_friend_request, unfriend_user, search_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('Login.urls')),
    path('', home, name ='home'),
    path('friends/', friendsPage, name = 'friendsPage'),
    path('notifications/', Notif, name = 'notif'),
    path('clearNotifications', clearNotifications, name = 'clearnotifications'),
    path('accept_friend_request/<int:notif_id>/', acceptFriendRequest, name='acceptFriendRequest'),
    path('delete_notification/<int:notif_id>/', deleteNotification, name='deleteNotification'),
    path('profile/<int:user_id>/', Profile, name = 'profile_with_id'),
    path('profile/', Profile, name='profile'),
    path('unfriend/<int:user_id>/', unFriend, name = 'unfriend'),
    path("upload_post/", uploadPost, name = "uploadPost"),
    path('delete_post/<int:post_id>/', deletePost, name = 'deletePost'),
    path('send_friend_request/', send_friend_request, name='send_friend_request'),
    path('unfriend_user/', unfriend_user, name='unfriend_user'),
    path('search/', search_user, name='search_user'),

]
