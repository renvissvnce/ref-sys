from django.shortcuts import render, redirect
from helpers.decorators import auth_user_should_not_access
from django.urls import reverse
from .models import Acc, Passcode
from django.contrib.auth import authenticate, login, logout



import random
from django.contrib import messages

characters = list('abcdefghijklmnopqrstuvwxyz1234567890')
characters2 = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890')
length = 6




def index(request):
    return render(request, 'main/index.html')


def acc(request):
    invite_code = Acc.objects.all()
    return render(request, 'main/account.html', {'invite_code': invite_code})



#Генерация инвайт-кода
def generate_invite_code() -> str:
    code = ''
    for x in range(length):
        code += random.choice(characters)
    return code

#Генерация смс-кода
def generate_invite_passcode() -> str:
    code = ''
    for x in range(length):
        code += random.choice(characters2)
    return code



@auth_user_should_not_access
def register(request):
    if request.method == "GET":
        generated_pass_code = generate_invite_passcode()
        passcode = Passcode(passcode=generated_pass_code)
        passcode.save()
        return render(request, 'main/register.html', {'pass': generated_pass_code})


    if request.method == "POST":
        context = {'has_error': False, 'data': request.POST}
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        invite_code = request.POST.get('invite_code')
        passcode = request.POST.get('passcode')

#Проверка смс-кода
        if not passcode:
            messages.add_message(request, messages.ERROR,
                                 'passcode is incorrect')
            context['has_error'] = True
            return render(request, 'main/error1.html', context, status=409)

        elif not Passcode.objects.filter(passcode=passcode).exists():
            messages.add_message(request, messages.ERROR,
                                 'Invite-code is incorrect')
            context['has_error'] = True
            return render(request, 'main/error.html')

#Проверка инвайт-кода
        if not invite_code:
            invite_code = generate_invite_code()

        """elif Acc.objects.filter(invite_code=invite_code).exists():
            messages.add_message(request, messages.ERROR,
                                 'Invite-code is incorrect')
            context['has_error'] = True
            return render(request, 'main/invite_code.html', context, status=409)"""

        if not Acc.objects.filter(invite_code=invite_code).exists():

            messages.add_message(request, messages.ERROR,
                                 'Invite-code is incorrect')
            context['has_error'] = True
            return render(request, 'main/ncorrect.html', context, status=409)


#Условие ввода пароля
        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'Password should be at least 6 characters')
            context['has_error'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'Password mismatch')
            context['has_error'] = True
#Условие ввода никнейма
        if not username:
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True

        if Acc.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'Username is taken, choose another one')
            context['has_error'] = True

            return render(request, 'main/register.html', context, status=409)
        if context['has_error']:
            return render(request, 'main/register.html', context)
#Отправка(сохранение) записей в базу данных
        user = Acc.objects.create_user(username=username, invite_code=invite_code, phone=phone)
        user.set_password(password)
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Account created')
        return redirect('login')
    return render(request, 'main/register.html')





@auth_user_should_not_access
def login_user(request):
    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.add_message(request, messages.ERROR, 'Invalid credentials, try again')

            return render(request, 'main/login.html', context, status=401)

        login(request, user)

    return render(request, 'main/login.html')



def logout_user(request):
    logout(request)

    messages.add_message(request, messages.SUCCESS,
                         'Successfully logged out')

    return redirect(reverse('login'))
