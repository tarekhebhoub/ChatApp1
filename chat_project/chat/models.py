from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class User(AbstractUser):
    pic = models.ImageField(upload_to='images/',null=True)
    
    def __str__(self):
    	return self.username


class Room(models.Model):
	name_room=models.CharField(max_length=255)
	isGroupeChat=models.BooleanField(default=False)
	owner=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
	users=models.ManyToManyField(get_user_model(),related_name='users_in_rooms')
	timestamp = models.DateTimeField(auto_now_add=True)
	latestMessage=models.ForeignKey('Message',on_delete=models.CASCADE,null=True,related_name='the_last_message')
	def __str__(self):
		return self.name_room
	

   

class Message(models.Model):
	content=models.CharField(max_length=255)
	timestamp = models.DateTimeField(auto_now_add=True)
	sender=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='the_sender')
	room=models.ForeignKey(Room,on_delete=models.CASCADE,related_name='the_room')
	readBy=models.ForeignKey(User,on_delete=models.CASCADE,related_name='the_readers',null=True)
	def __str__(self):
		return self.content