import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from Config import LDAPSettings
from auth_ldap.LDAP.LDAPBackend import backend_1
from auth_ldap.LDAP.LDAPBackend import backend_2
from django.contrib.auth import get_user_model


def login_page(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('home')
        else:
            context = {}
            return render(request, 'registration/login_page.html', context)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        is_remember = request.POST.getlist('remember')

        user_login = None

        if LDAPSettings.is_auth_with_LDAP:
            user_login1 = backend_1.authenticate(username, password)
            user_login2 = backend_2.authenticate(username, password)

            if user_login1 is None and user_login2 is None:
                messages.error(request, 'Неверный логин или пароль')
                return redirect('login_page')

            if user_login1 is None:
                user_login = user_login2

            if user_login2 is None:
                user_login = user_login1
        else:
            # TODO: Убрать при загрузке на продакшн
            User = get_user_model()
            user_login = User.objects.filter(username=username).first()
            if user_login is None:
                user_login = User(username=username,
                                  password=password,
                                  is_active=True)
                user_login.save()
            if user_login.password != password:
                messages.error(request, 'Неверный логин или пароль')
                return redirect('login_page')

        if is_remember:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)

        login(request, user_login)
        messages.success(request, 'Добро пожаловать!')
        return redirect('login_page')

    messages.error(request, 'Не определён метод запроса')
    return redirect('login_page')


@login_required(login_url='login_page')
def logout_page(request):
    logout(request)
    return redirect('login_page')
