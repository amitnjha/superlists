from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from accounts.models import Token
from django.urls import reverse
import sys
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
# Create your views here.


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email = email)
    url = request.build_absolute_uri(reverse('login') + '?token=' + str(token.uid))
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists',
        [email]
        )
    messages.success(request, "Check your email, we have sent you a link you can use to log in")
    return redirect('/superlists/')

def login(request):
    print('login view', file = sys.stderr)
    uid = request.GET.get('token')
    print('uid',uid)
    
    user = authenticate(request,uid = uid)
    print('user is', user)
    if user is not None:
        auth_login(request, user)
    #return redirect('/')
    return redirect('/superlists/')

def logout(request):
    auth_logout(request)
    return redirect('/superlists/')

