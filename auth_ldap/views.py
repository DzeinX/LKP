from django.shortcuts import render


def login_page(request):
    context = {}
    return render(request, 'auth/login_page.html', context)
