from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def main(request):
    context = {}
    return render(request, 'lkp_logic/main.html', context)

@login_required
def home(request):
    context = {}
    return render(request, 'templates/home.html', context)

@login_required
def baseTemplate(request):
    context = {}
    return render(request, 'templates/Base_template.html', context)

@login_required
def app(request):
    context = {}
    return render(request, 'templates/app.html', context)

@login_required
def loginPage(request):
    context = {}
    return render(request, 'templates/registration/login_page.html', context)

@login_required
def create(request):
    context = {}
    return render(request, 'templates/lkp_logic/create.html', context)
@login_required
def critery(request):
    context = {}
    return render(request, 'templates/lkp_logic/critery.html', context)
@login_required
def criteryCategory(request):
    context = {}
    return render(request, 'templates/lkp_logic/critery_category.html', context)
@login_required
def edit(request):
    context = {}
    return render(request, 'templates/lkp_logic/edit.html', context)
@login_required
def editAdd(request):
    context = {}
    return render(request, 'templates/lkp_logic/edit-add.html', context)
@login_required
def efficiency(request):
    context = {}
    return render(request, 'templates/lkp_logic/efficiency.html', context)
@login_required
def portfolio(request):
    context = {}
    return render(request, 'templates/lkp_logic/portfolio.html', context)
@login_required
def report(request):
    context = {}
    return render(request, 'templates/lkp_logic/report.html', context)

@login_required
def show(request):
    context = {}
    return render(request, 'templates/lkp_logic/show.html', context)