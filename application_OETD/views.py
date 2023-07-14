from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from application_OETD.models import *

@login_required(login_url='login_page')
def main(request):
    context = {}
    return render(request, 'lkp_logic/main.html', context)


@login_required
def home(request):
    context = {}
    return render(request, 'home.html', context)


@login_required
def base_template(request):
    context = {}
    return render(request, 'Base_template.html', context)


@login_required
def app(request):
    context = {}
    return render(request, 'app.html', context)


@login_required
def login_page(request):
    context = {}
    return render(request, 'registration/login_page.html', context)


@login_required
def create(request):
    context = {}
    return render(request, 'lkp_logic/create.html', context)


@login_required
def critery(request):
    context = {}
    return render(request, 'lkp_logic/critery.html', context)


@login_required
def critery_category(request):
    context = {}
    return render(request, 'lkp_logic/critery_category.html', context)


@login_required
def edit(request):
    context = {}
    return render(request, 'lkp_logic/edit.html', context)


@login_required
def edit_add(request):
    context = {}
    return render(request, 'lkp_logic/edit-add.html', context)


@login_required
def efficiency(request):
    context = {}
    return render(request, 'lkp_logic/efficiency.html', context)


@login_required
def portfolio(request,_id):
    if request.method == "GET":
        file_categories = FilesCatigories.objects.all()
        files = Files.objects.filter(user_id =_id)

        context = {
            'file_caregories' : file_categories,
            'files' : files
        }
    return render(request, 'lkp_logic/portfolio.html', context)



@login_required (login_url='login_page')
def report(request,_id):
    if request.method == "GET":
        categories = Categories.objects.all()
        form = Forms.objects.get(id =_id)
    context = {
        "categories" : categories,
        "form" : form
    }
    return render(request, 'lkp_logic/report.html', context)


@login_required
def show(request):
    context = {}
    return render(request, 'lkp_logic/show.html', context)

@login_required
def file_delete(request, pk):
    file = get_object_or_404(Files, pk=pk)
    if request.method == "POST":
        file.delete()
    return redirect ('portfolio')     
   