from django.db import models
from django.contrib.auth.models import User

class FriendsList(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='friends_list')
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    def __str__(self):
        return f"{self.user.username}'s friends"
    
    def add_friend(self, friend):
        if friend not in self.friends.all():
            self.friends.add(friend)
            self.save()
    
    def remove_friend(self, friend):
        if friend in self.friends.all():
            self.friends.remove(friend)
            self.save()
    
    def unfriend(self, friend):
        B = FriendsList.objects.get(user = friend)
        B.remove_friend(self.user)
        self.remove_friend(friend)

    def is_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False
    
    def are_friends(self, friends_collection):
        mutual_friends = self.friends.filter(id__in=friends_collection.values_list('id', flat=True))
        return mutual_friends
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    Type = models.CharField(max_length=255, related_name= 'type')
    _from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_from')
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.Type
    
class PendingNotif(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notifications')
    notifications = models.ManyToManyField(Notification, related_name='pending_notifs', blank=True)

    def __str__(self):
        return f"{self.user.username}'s pending notifications"