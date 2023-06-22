import hashlib

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

import Config
from auth_ldap.LDAP.LDAPBackend import backend_1
from auth_ldap.LDAP.LDAPBackend import backend_2
from django.contrib.auth import get_user_model


def login_page(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('main')
        else:
            context = {}
            return render(request, 'registration/login_page.html', context)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user_login = None

        if Config.LDAPSettings.is_LDAP:
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
            user = get_user_model()
            user_login = user.objects.filter(username=username).first()
            if user_login is None:
                user_login = user(username=username,
                                  is_superuser=False,
                                  password=password,
                                  is_staff=True,
                                  is_active=True)
                user_login.save()
            if user_login.password != password:
                messages.error(request, 'Неверный логин или пароль')
                return redirect('login_page')

        login(request, user_login)
        messages.success(request, 'Добро пожаловать!')
        return redirect('login_page')

    messages.error(request, 'Не определён метод запроса')
    return redirect('login_page')


@login_required
def logout_page(request):
    logout(request)
    return redirect('login_page')
