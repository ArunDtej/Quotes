from django.db import models
from django.contrib.auth.models import User

class Comments(models.Model):
    #commented by 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_list')
    #comment
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.post.id} at {self.created_at}"



class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reactors = models.ManyToManyField(User, related_name='reacted_users', blank=True)
    comments = models.ManyToManyField(Comments, related_name='reacted_users', blank=True)

    def add_reactor(self, reactor):
        if reactor not in self.reactors.all():
            self.reactors.add(reactor)
            self.save()

    def remove_reactor(self, reactor):
        if reactor in self.reactors.all():
            self.reactors.remove(reactor)
            self.save()

    def is_reacted(self, reactor):
        if reactor in self.reactors.all():
            return True
        return False
    
    def __str__(self):
        return f"{self.user.username} post at {self.created_at}"
    
    def add_comment(self, comment):
        self.comments.add(comment)

    def remove_comment(self, comment):
        self.comments.remove(comment)

    def get_comments(self):
        return self.comments.all()

    def get_reacts(self):
        return self.reactors.all()

    def get_reacts_count(self):
        return len(self.reactors.all())
    
    def get_comments_count(self):
        return len(self.comments.all())
    
class FriendsList(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='friends_list')
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    def __str__(self):
        return f"{self.user.username}'s friends"
    
    def add_friend(self, friend):
        if friend not in self.friends.all():
            notification = Notification(user = friend, Type = "Request", from_user = self.user)
            notification.save()

    def accept_request(self,friend: User):
        if friend not in self.friends.all():
            self.friends.add(friend)
            self.save()

            B = FriendsList.objects.get(user = friend)
            B.friends.add(self.user)
            B.save()

    
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
        if friends_collection is None:
            return False
        
        # If friends_collection is a single user object, handle that case
        if isinstance(friends_collection, User):
            return self.is_friend(friends_collection)
        
        # If friends_collection is a queryset or list, handle that case
        if hasattr(friends_collection, 'values_list'):
            mutual_friends = self.friends.filter(id__in=friends_collection.values_list('id', flat=True))
            return mutual_friends.exists()
        
        # If friends_collection is neither a single user nor a queryset, return False
        return False
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'notifications')
    Type = models.CharField(max_length=255)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_from')
    created_at = models.DateTimeField(auto_now_add=True)
    post_id = models.IntegerField(blank=True, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        if self.Type == "Request":
            return f"{self.from_user} sent you a friend request at {self.created_at}"
        elif self.Type == "React":
            return f"{self.from_user} reacted to you a post"
        elif self.Type == "Comment":
            return f"{self.from_user} commented on your post"
        return self.Type
    
