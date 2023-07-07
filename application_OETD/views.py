from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.shortcuts import render,redirect
from auth_ldap.models import User as current_user
from .models import *
from django.contrib import messages


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

    if request.method == "GET":
        categories = FilesCatigories.objects.all()
        context = {'categories': categories}
        return render(request, 'lkp_logic/create.html', context)

    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        date_now = datetime.now()
        document = request.FILES["file"]
        document_name = default_storage.save(f'{request.user.id}.{document.name.split(".")[1]}',document)
        file_category_id = request.POST["file_category_id"]

        try:
            file_category = FilesCatigories.objects.get(id=file_category_id)
            user = current_user.objects.get(id=request.user.id)
            Files.objects.create(created_at=date_now,
                                 updated_at=date_now,
                                 path=document_name,
                                 name=name,
                                 description=description,
                                 file_category_id=file_category,
                                 user_id=user)
        except Exception as e:
            messages.error(request,f'Данные не сохранены.Ошибка: {e}')
            return redirect('create')
        messages.success(request,f'Данные успешно сохранены')
        return redirect('create')
    messages.error(request, f'Не опредленный метод запроса')
    return redirect('create')






@login_required
def critery(request):
    if request.method == "GET":
        fields = Fields.objects.all()
        categories = FilesCatigories.objects.all()
        context = {'categories': categories,
                   'fields':fields}
        return render(request, 'lkp_logic/critery.html', context)
    messages.error(request, f'Не опредленный метод запроса')
    return redirect('critery')

@login_required
def critery_category(request,_id):
    if request.method == "GET":
        form = Forms.objects.get(id = _id)
        fields = Fields.objects.filter(form_id = form.id).all()
        form_categories = list(FormCategory.objects.filter(form_id = form.id).all())
        print(form_categories[0].category_id)
        # categories = [Categories.objects.get(id =int(category.category_id)) for category in form_categories ]
        categories = [category.category_id for category in form_categories ]
        context = {'form':form,
                   'field':fields,
                   'categories':categories
                   }
        return render(request, 'lkp_logic/critery_category.html', context)
    messages.error(request, f'Не опредленный метод запроса')
    return redirect('critery_category')

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
def portfolio(request):
    context = {}
    return render(request, 'lkp_logic/portfolio.html', context)


@login_required
def report(request):
    context = {}
    return render(request, 'lkp_logic/report.html', context)


@login_required
def show(request):
    context = {}
    return render(request, 'lkp_logic/show.html', context)
