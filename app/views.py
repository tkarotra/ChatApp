from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import JsonResponse

# Create your views here.

def Register(request):
    if request.method =="POST":
        return redirect('login')
    # else:
    #     return render(request, 'app/register.html')

def Login(request):
    if 'username' not in request.session:
        if request.method == "POST":
            # p = User.objects.raw('SELECT * FROM app_user WHERE username like ""')
            username = request.POST['username'].lower()
            password = request.POST['password']
            if username and password:
                try:
                    user = User.objects.get(Username = username)
                except:
                    messages.error(request, 'User does not exist. Register to continue.')
                    return redirect('register')
                if user.Password == password:
                    request.session['username'] = user.Username
                    request.session['id'] = user.id
                    return redirect('chat')
                else:
                    messages.error(request, 'Password entered is incorrect.')
                    return redirect('login')
            else:
                messages.error(request, 'All fields are mandatory.')
                return redirect('login')
        else:
            return render(request, 'app/login.html')
    else:
        return redirect('chat')

def Logout(request):
    if 'username' in request.session:
        del(request.session['username'])
        del(request.session['id'])
        messages.success(request, 'Logged out successfully.')
        return redirect('login')
    else:
        return redirect('login')

def Chat(request):
    if 'username' in request.session:
        if request.method == 'POST':
            chat_room_id = request.POST['chat_room_id']
            room_obj = ChatRoom.objects.get(id=chat_room_id)
            if room_obj.LastMessageBy.Username != request.session['username']:
                room_obj.MessageRead = True
                room_obj.save()

            messages = Message.objects.filter(Room_ID = chat_room_id)
            list_of_messages = []
            for i in messages:
                item = {
                    'sent_by': i.Sent_By_id,
                    'text': i.Message_Text,
                    'datetime': i.Sent_DateTime
                }
                list_of_messages.append(item)
            return JsonResponse({'data': list_of_messages, 'last': room_obj.LastMessageBy.id})
        else:
            print(ChatRoom.user_objects.by_user(request.session['id']))
            room = ChatRoom.user_objects.by_user(request.session['id'])
            return render(request, "app/base.html", {'rooms': room})
    else:
        return redirect('login')