from datetime import datetime

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
            user = User.objects.get(id=request.user.id)
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






@login_required(login_url='login_page')
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


@login_required(login_url='login_page')
def edit(request):
    if request.method == "GET":
        positions = Positions.objects.all()
        departments = Departments.objects.all()
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
            position = Positions.objects.get(id=position_id)
            departament = Departments.objects.get(id=departament_id)

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
        forms = Forms.objects.all()

        access_forms = []
        for form in forms:
            fields = Fields.objects.filter(form_id=form.id).all()
            reporting_period = ReportingPeriods.objects.get(id=form.reporting_period_id)
            form_position = FormPosition.objects.filter(position_id=request.user.position_id, form_id=form.id).first()
            inspector_id = request.user.inspector_id

            access = []
            if inspector_id is not None:
                access = [field if field.inspector_id == inspector_id else None for field in fields]

            if len(access) == access.count(None):
                # Точно не может проверить форму
                if reporting_period.active and form_position is not None:
                    # Может заполнить
                    access_forms.append([form, True, False])
                else:
                    # Не может заполнить
                    access_forms.append([form, False, False])
            else:
                # Точно может проверить форму
                if reporting_period.active and form_position is not None:
                    # Может заполнить
                    access_forms.append([form, True, True])
                else:
                    # Не может заполнить
                    access_forms.append([form, False, True])

            # access_forms -> [[форма, может_заполнить, может_проверить], [...], ...]

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
        field = Fields.objects.get(id=_id)

        if field.inspector_id == request.user.inspector_id:
            users = User.objects.all()
            form = Forms.objects.get(id=field.id)

            access_users = []
            for user in users:
                values = list(Values.objects.filter(user_id=user.id, field_id=field.id).all())
                categories_values = []
                for value in values:
                    category = Categories.objects.get(id=value.id)
                    category_value = {
                        'category': category,
                        'value': value
                    }
                    categories_values.append(category_value)
                access_users.append([user, categories_values])

            context = {
                "field": field,
                "users": access_users,
                "form": form
            }
            return render(request, 'lkp_logic/show.html', context)

        messages.error(request, 'У вас нет доступа к этому критерию')
        return redirect('home')

    if request.method == "POST":


        messages.success(request, 'Данные успешно сохранены!')
        return redirect('show')

    messages.error(request, 'Не определён метод запроса')
    return redirect('home')
