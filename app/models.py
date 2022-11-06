from django.db import models
from django.core.exceptions import ValidationError
import datetime as dt
from datetime import datetime
from django.db.models import Q
# from django import forms

# Create your models here.

class User(models.Model):
    Email = models.EmailField(max_length=40, default="")
    Name = models.CharField(max_length=100, default="")
    Username = models.CharField(max_length=30, default="", unique=True)
    Password = models.CharField(max_length=250, default="")
    Profile_Picture = models.FileField(upload_to="media/", null=True, blank=True)
    Date_of_Birth = models.DateField(default=datetime.now(), null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Creation_DateTime = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.Username


class RoomManager(models.Manager):
    def by_user(self, user):
        # user = request.session.get('id')
        lookup = Q(User_1__id=user) | Q(User_2__id=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs

class ChatRoom(models.Model):
    User_1 = models.ForeignKey(User, related_name="user_1", on_delete=models.SET_DEFAULT, default="1")
    User_2 = models.ForeignKey(User, related_name="user_2", on_delete=models.SET_DEFAULT, default="1")
    Creation_DateTime = models.DateTimeField(default=datetime.now())
    
    LastMessageBy = models.ForeignKey(User, related_name="last_user", on_delete=models.SET_DEFAULT, default="1", null=True, blank=True)
    MessageRead = models.BooleanField(default=False)
    Sent_DateTime = models.DateTimeField(default=datetime.now())

    objects = models.Manager()
    user_objects = RoomManager()

    def clean(self):
        user1 = self.User_1
        user2 = self.User_2

        pair1 = Q(User_1 = user1) & Q(User_2 = user2)
        pair2 = Q(User_1 = user2) & Q(User_2 = user1)
        check_pair = Q(pair1 | pair2)
        pair = ChatRoom.objects.filter(check_pair)

        if pair.exists():
            print(pair[0].id, self.id)
            if self.id == None:
                raise ValidationError({
                    'User_1': f'Pair between {user1} and {user2} already exists',
                    'User_2': ''
                })
            else:
                if (pair[0].id != self.id):
                    raise ValidationError({
                        'User_1': f'Pair between {user1} and {user2} already exists',
                        'User_2': ''
                    })


    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    # class Meta:
    #     unique_together = ['User_1', 'User_2']

    # def __str__(self):
    #     return self.id



class Message(models.Model):
    Room_ID = models.ForeignKey(ChatRoom, related_name="room", on_delete=models.SET_DEFAULT, default="1")
    Sent_By = models.ForeignKey(User, related_name="user", on_delete=models.SET_DEFAULT, default="1")
    Message_Text = models.TextField()
    Sent_DateTime = models.DateTimeField(default=datetime.now())