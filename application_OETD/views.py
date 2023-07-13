from datetime import datetime
import pandas as pd
from io import StringIO
import xlsxwriter
import os
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.core.files.storage import default_storage
from django.shortcuts import render, redirect

from .models import *
from django.contrib import messages


@login_required(login_url='login_page')
def main(request):
    context = {}
    return render(request, 'lkp_logic/main.html', context)


@login_required(login_url='login_page')
def home(request):
    context = {}
    return render(request, 'home.html', context)


@login_required(login_url='login_page')
def base_template(request):
    context = {}
    return render(request, 'Base_template.html', context)


@login_required(login_url='login_page')
def app(request):
    context = {}
    return render(request, 'app.html', context)


@login_required(login_url='login_page')
def login_page(request):
    context = {}
    return render(request, 'registration/login_page.html', context)


@login_required(login_url='login_page')
def create(request):
    if request.method == "GET":
        categories = FileCategory.objects.all()
        context = {'categories': categories}
        return render(request, 'lkp_logic/create.html', context)

    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        date_now = datetime.now()
        document = request.FILES["file"]
        document_name = default_storage.save(f'{request.user.id}.{document.name.split(".")[1]}', document)
        file_category_id = request.POST["file_category_id"]

        try:
            file_category = FileCategory.objects.get(id=file_category_id)
            user = User.objects.get(id=request.user.id)
            File.objects.create(created_at=date_now,
                                updated_at=date_now,
                                path=document_name,
                                name=name,
                                description=description,
                                file_category_id=file_category,
                                user_id=user)
        except Exception as e:
            messages.error(request, f'Данные не сохранены.Ошибка: {e}')
            return redirect('create')
        messages.success(request, f'Данные успешно сохранены')
        return redirect('create')
    messages.error(request, f'Не определён метод запроса')
    return redirect('create')


@login_required(login_url='login_page')
def criteria(request,_id):
    if request.method == "GET":
        form = Forms.objects.get(id=_id)
        fields = Fields.objects.filter(form_id = form.id).all()
        form_categories = list(FormCategory.objects.filter(form_id=form.id).all())
        categories =[]
        for category in form_categories:
            categories.append(Categories.objects.get(id =int(category.category_id)))
        context = {'categories': categories,
                   'fields':fields}
        return render(request, 'lkp_logic/criteria.html', context)
    if request.method =="POST":
        category_id = request.POST["category"]
        category = Categories.objects.get(id=category_id)
        values = Values.objects.filter(category_id=category.id).all()
        data = {"ФИО": [],
                "Должность": []}
        for value in values:
            field_id = value.field_id
            field = Fields.objects.get(id=field_id)
            data[f"{field.name}"] = []
            data[f"{value.comment}"] = []
        for user in User.objects.all():
            data["ФИО"].append(user.full_name)
            data["Должность"].append(user.department)
            for value in values:
                if value.user_id==user.id:
                    field_id = value.field_id
                    field = Fields.objects.get(id=field_id)
                    data[f"{field.name}"].append(value.value)
                    data[f"{value.comment}"].append(value.comment)
        df = pd.DataFrame(data)
        df.to_excel(f"static/Отчет по {category} за {datetime.datetime.now().date()}.xlsx", index=False)
        with open(f"static/Отчет по {category} за {datetime.datetime.now().date()}.xlsx", 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(f"static/Отчет по {category} за {datetime.datetime.now().date()}.xlsx")
            return response
    messages.error(request, f'Не опредленный метод запроса')
    return redirect('criteria',_id)


@login_required
def criteria_category(request, _id):
    if request.method == "GET":
        form = Forms.objects.get(id = _id)
        fields = Fields.objects.filter(form_id = form.id).all()
        form_categories = list(FormCategory.objects.filter(form_id = form.id).all())
        categories = []
        for category in form_categories:
            categories.append(Categories.objects.get(id =int(category.category_id)))

        context = {'form':form,
                   'fields':fields,
                   'categories':categories,
                   }
        return render(request, 'lkp_logic/criteria_category.html', context)
    if request.method == "POST":
        form_id = request.POST['form_id'].split('-')


        try:
            messages.success(request, f'Успешно')
            return redirect('criteria_category', _id)
        except Exception as e:
            messages.error(request, f'Не удалось сохранить данные. Ошибка: {e}')
            return redirect('criteria_category', _id)
    messages.error(request, f'Не опредленный метод запроса')
    return redirect('criteria_category',_id)


@login_required(login_url='login_page')
def edit(request):
    if request.method == "GET":
        positions = Position.objects.all()
        departments = Department.objects.all()
        context = {
            'positions': positions,
            'departments': departments
        }
        return render(request, 'lkp_logic/edit.html', context)

    if request.method == "POST":
        position_id = request.POST['position_id']
        departament_id = request.POST['departament_id']
        orcid = request.POST['orcid']
        wosrid = request.POST['wosrid']
        said = request.POST['said']
        spin = request.POST['spin']

        try:
            position = Position.objects.get(id=position_id)
            departament = Department.objects.get(id=departament_id)

            request.user.position_id = position
            request.user.departament_id = departament
            request.user.orcid = orcid
            request.user.wosrid = wosrid
            request.user.said = said
            request.user.spin = spin

            request.user.save()
        except Exception as e:
            messages.error(request, f'Не удалось сохранить данные. Ошибка: {e}')
            return redirect('edit')

        messages.success(request, 'Данные успешно сохранены!')
        return redirect('edit')

    messages.error(request, 'Не определён метод запроса')
    return redirect('home')


@login_required(login_url='login_page')
def edit_add(request):
    context = {}
    return render(request, 'lkp_logic/edit-add.html', context)


@login_required(login_url='login_page')
def efficiency(request):
    if request.method == "GET":
        forms = Form.objects.all()

        access_forms = []
        for form in forms:
            fields = Field.objects.filter(form_id=form.id).all()
            reporting_period = ReportingPeriod.objects.get(id=form.reporting_period_id)
            form_position = FormPosition.objects.filter(position_id=request.user.position_id, form_id=form.id).first()
            inspector_id = request.user.inspector_id

            access = []
            if inspector_id is not None:
                access = [field if field.inspector_id == inspector_id else None for field in fields]

            is_can_fill = True if reporting_period.active and form_position is not None else False
            is_can_check = True if len(access) != access.count(None) else False
            is_can_read = not is_can_fill

            access_forms.append([form, is_can_fill, is_can_check, is_can_read])

            # access_forms -> [[форма, может_заполнить, может_проверить, может_просмотреть], [...], ...]

        context = {
            'forms': access_forms
        }
        return render(request, 'lkp_logic/efficiency.html', context)

    messages.error(request, 'Не определён метод запроса')
    return redirect('home')


@login_required(login_url='login_page')
def portfolio(request, _id):
    context = {}
    return render(request, 'lkp_logic/portfolio.html', context)


@login_required(login_url='login_page')
def report(request):
    context = {}
    return render(request, 'lkp_logic/report.html', context)


@login_required(login_url='login_page')
def show(request, _id):
    if request.method == "GET":
        field = Field.objects.get(id=_id)

        if field.inspector_id == request.user.inspector_id:
            users = User.objects.all()
            form = Form.objects.get(id=field.id)

            access_users = []
            for index, user in enumerate(users):
                values = list(Value.objects.filter(user_id=user.id, field_id=field.id).all())
                if not values:
                    continue

                categories_values = []
                for value in values:
                    category = Category.objects.get(id=value.category_id)
                    category_value = {
                        'category': category,
                        'value': value
                    }
                    categories_values.append(category_value)
                access_users.append([user, categories_values, index + 1])

            context = {
                "field": field,
                "users": access_users,
                "form": form
            }
            return render(request, 'lkp_logic/show.html', context)

        messages.error(request, 'У вас нет доступа к этому критерию')
        return redirect('home')

    if request.method == "POST":
        form_id = request.POST['form_id'].split('-')

        # if request.POST.get("save_all"):
        #     form_length = request.POST['form_length']

        try:
            category_id = request.POST[f'category_id-{form_id[0]}']
            user_id = request.POST[f'user_id-{form_id[0]}']
            new_value = request.POST[f'value-{form_id[0]}-{form_id[1]}'].replace(' ', '').rstrip()

            if new_value:
                user_answer = Value.objects.filter(user_id=user_id, category_id=category_id).first()
                user_answer.value = new_value
                user_answer.save()
            else:
                messages.error(request, f'Значение введено некорректно')
                return redirect('show', _id)

        except Exception as e:
            messages.error(request, f'Не удалось сохранить данные. Ошибка: {e}')
            return redirect('show', _id)

        messages.success(request, 'Данные успешно сохранены!')
        return redirect('show', _id)

    messages.error(request, 'Не определён метод запроса')
    return redirect('home')

