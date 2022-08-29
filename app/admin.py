from django.contrib import admin
from .models import *
from django.db.models import Q
from django import forms

# Register your models here.

# class ChatRoomForm(forms.ModelForm):
#     class Meta:
#         model = ChatRoom

#         def clean(self):

class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('Name', 'Email', 'Username', 'Creation_DateTime', 'Password')
        }),
        ('Advanced Details', {
            'classes': ('collapse'),
            'fields': ('Profile_Picture', 'Date_of_Birth', 'Description')
        })
    )
    list_display = ('Name', 'Email', 'Username', 'Creation_DateTime')
    list_filter = ('Creation_DateTime', 'Email')
    search_fields = ('Name', 'Username')  # User_1__Username 

class ChatMessage(admin.TabularInline):
    model = Message

class ChatRoomAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = ChatRoom

admin.site.register(User, UserAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message)