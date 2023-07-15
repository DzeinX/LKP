from datetime import datetime
from transliterate import translit
import pandas as pd
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


@login_required(login_url='login_page')
def home(request):
    context = {}
    return render(request, 'home.html', context)


@login_required(login_url='login_page')
def create_file(request):
    if request.method == "GET":
        categories = FileCategory.objects.all()
        context = {'categories': categories}
        return render(request, 'lkp_logic/create_file.html', context)

    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        date_now = datetime.datetime.now()
        document = request.FILES["file"]
        default_storage.save(f'{request.user.id}.{document.name.split(".")[1]}', document)
        file_category_id = request.POST["file_category_id"]

        try:
            file_category = FileCategory.objects.get(id=file_category_id)
            file = File.objects.create(created_at=date_now,
                                       updated_at=date_now,
                                       name=name,
                                       description=description,
                                       file_category_id=file_category.id,
                                       user_id=request.user.id)
            file.save()
        except Exception as e:
            messages.error(request, f'Данные не сохранены.Ошибка: {e}')
            return redirect('create_file')

        messages.success(request, f'Данные успешно сохранены')
        return redirect('portfolio', request.user.id)

    messages.error(request, f'Не определён метод запроса')
    return redirect('create_file')


@login_required(login_url='login_page')
def checking_questionnaire(request, _id):
    if request.method == "GET":
        form = Form.objects.get(id=_id)

        is_can_check = is_user_can_check_questionnaire(form, request.user)
        access = is_user_has_access(form, request.user)
        if is_can_check and access:
            fields = Field.objects.filter(form_id=form.id).all()
            form_categories = list(FormCategory.objects.filter(form_id=form.id).all())
            categories = []
            for category in form_categories:
                categories.append(Category.objects.get(id=int(category.category_id)))
            context = {'categories': categories,
                       'fields': fields}
            return render(request, 'lkp_logic/checking_questionnaire.html', context)

        messages.error(request, f'У вас нет доступа к этой анкете')
        return redirect('home')

    if request.method == "POST":
        category_id = request.POST["category"]
        category = Category.objects.get(id=category_id)

        file_name = f"Отчет по {str(category.name)} за {datetime.datetime.now().date()}.xlsx"

        create_report_as_xlsx(form_id=_id,
                              file_name=file_name)

        with open('static/' + file_name, 'rb') as fh:
            content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            response = HttpResponse(fh.read(),
                                    content_type=content_type)
            response['Content-Disposition'] = "inline; filename=" + translit(file_name,
                                                                             language_code='ru',
                                                                             reversed=True)
        return response

    messages.error(request, f'Не определён метод запроса')
    return redirect('checking_questionnaire', _id)


def create_report_as_xlsx(form_id: int, file_name: str) -> None:
    data = {
        "ФИО": [],
        "Должность": []
    }

    fields = Field.objects.filter(form_id=form_id).all()
    for index, field in enumerate(fields):
        data[f"{field.name}"] = []
        data[f"Комментарий {index + 1}"] = []

    for user in User.objects.all():
        data["ФИО"].append(user.full_name if user.full_name is not None else user.username)
        data["Должность"].append(user.department.name if user.department is not None else '')

        index = 1
        for field in fields:
            value = Value.objects.filter(field_id=field.id, user_id=user.id).first()
            if value is not None:
                if value.user_id == user.id:
                    field_id = value.field_id
                    field = Field.objects.get(id=field_id)
                    data[f"{field.name}"].append(value.value if value.value is not None else 0)
                    data[f"Комментарий {index}"].append(value.comment if value.comment is not None else '')
                    index += 1
            else:
                data[f"{field.name}"].append(0)
                data[f"Комментарий {index}"].append('')
                index += 1

    df = pd.DataFrame(data)

    if '.' in file_name:
        df.to_excel(f"static/{file_name}", index=False)
    else:
        df.to_excel(f"static/{file_name}.xlsx", index=False)


@login_required(login_url='login_page')
def filling_questionnaire(request, _id):
    if request.method == "GET":
        form = Form.objects.get(id=_id)

        if is_user_has_access(form, request.user):
            fields = Field.objects.filter(form_id=form.id).all()

            field_value = []
            for field in fields:
                value = Value.objects.filter(field_id=field.id, user_id=request.user.id).first()
                field_value.append([field, value])

            is_disabled = is_user_can_read_questionnaire(form, request.user)

            context = {
                'form': form,
                'field_value': field_value,
                'is_disabled': is_disabled
            }
            return render(request, 'lkp_logic/filling_questionnaire.html', context)

        messages.error(request, f'У вас нет доступа к этой анкете')
        return redirect('home')

    if request.method == "POST":
        form_id = request.POST['form_id']
        user_value = request.POST[f'value-{form_id}']
        field_id = request.POST[f'field_id-{form_id}']
        field = Field.objects.get(id=field_id)
        form = Form.objects.get(id=field.form_id)
        category = form.get_current_filling_period()

        if category.is_can_filling():
            try:
                value = Value.objects.filter(field_id=field.id, user_id=request.user.id).first()
                if value is None:
                    value = Value(field_id=field.id,
                                  user_id=request.user.id,
                                  value=user_value,
                                  lock=False,
                                  visible=True,
                                  category_id=category.id)
                else:
                    value.value = user_value
                value.save()
                messages.success(request, f'Данные успешно сохранены!')
                return redirect('filling_questionnaire', _id)

            except Exception as e:
                messages.error(request, f'Не удалось сохранить данные. Ошибка: {e}')
                return redirect('filling_questionnaire', _id)

        messages.error(request, f'Нельзя изменить данные в закрытой анкете')
        return redirect('filling_questionnaire', _id)

    messages.error(request, f'Не определён метод запроса')
    return redirect('filling_questionnaire', _id)


@login_required(login_url='login_page')
def edit_profile(request):
    if request.method == "GET":
        positions = Position.objects.all()
        departments = Department.objects.all()
        context = {
            'positions': positions,
            'departments': departments
        }
        return render(request, 'lkp_logic/edit_profile.html', context)

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
            return redirect('edit_profile')

        messages.success(request, 'Данные успешно сохранены!')
        return redirect('edit_profile')

    messages.error(request, 'Не определён метод запроса')
    return redirect('home')


@login_required(login_url='login_page')
def edit_add(request):
    context = {}
    return render(request, 'lkp_logic/edit-add.html', context)


@login_required(login_url='login_page')
def questionnaire(request):
    if request.method == "GET":
        forms = Form.objects.all()

        access_forms = []
        for form in forms:
            is_can_fill = is_user_can_fill_questionnaire(form, request.user)
            is_can_check = is_user_can_check_questionnaire(form, request.user)
            is_can_read = is_user_can_read_questionnaire(form, request.user)

            if is_user_has_access(form, request.user):
                access_forms.append([form, is_can_fill, is_can_check, is_can_read])
                # access_forms -> [[форма, может_заполнить, может_проверить, может_просмотреть], [...], ...]

        context = {
            'forms': access_forms
        }
        return render(request, 'lkp_logic/questionnaire.html', context)

    messages.error(request, 'Не определён метод запроса')
    return redirect('home')


def is_user_has_access(form: Form, user: User) -> bool:
    form_position = FormPosition.objects.filter(position_id=user.position_id, form_id=form.id).first()
    fields = Field.objects.filter(form_id=form.id).all()
    access = []
    if user.inspector_id is not None:
        access = [field if field.inspector_id == user.inspector_id else None for field in fields]
    return True if form_position is not None or len(access) != access.count(None) else False


def is_user_can_fill_questionnaire(form: Form, user: User) -> bool:
    category_filling_period = form.get_current_filling_period()
    form_position = FormPosition.objects.filter(position_id=user.position_id, form_id=form.id).first()

    is_can_fill = False
    if category_filling_period is not None:
        is_can_fill = True if category_filling_period.is_can_filling() and form_position is not None else False

    return is_can_fill


def is_user_can_check_questionnaire(form: Form, user: User) -> bool:
    category_checking_period = form.get_current_checking_period()
    fields = Field.objects.filter(form_id=form.id).all()
    access = []
    if user.inspector_id is not None:
        access = [field if field.inspector_id == user.inspector_id else None for field in fields]

    is_can_check = False
    if category_checking_period is not None:
        is_can_check = True if category_checking_period.is_can_checking() and len(access) != access.count(
            None) else False

    return is_can_check


def is_user_can_read_questionnaire(form: Form, user: User) -> bool:
    return not is_user_can_fill_questionnaire(form, user)


@login_required(login_url='login_page')
def portfolio(request, _id):
    if request.method == "GET":
        files = File.objects.filter(user_id=_id)
        user = User.objects.get(id=_id)

        context = {
            'files': files,
            'current_user': user
        }
        return render(request, 'lkp_logic/portfolio.html', context)


@login_required(login_url='login_page')
def report(request, _id):
    if request.method == "GET":
        categories = Category.objects.all()
        form = Form.objects.get(id=_id)
        context = {
            "categories": categories,
            "form": form
        }
        return render(request, 'lkp_logic/report.html', context)


@login_required(login_url='login_page')
def file_delete(request, _id, user_id):
    file = get_object_or_404(File, pk=_id)
    if request.method == "POST":
        file.delete()
    return redirect('portfolio', user_id)


@login_required(login_url='login_page')
def category_for_checking(request, _id):
    if request.method == "GET":
        field = Field.objects.get(id=_id)

        if field.inspector_id == request.user.inspector_id:
            users = User.objects.all()
            form = Form.objects.get(id=field.form_id)

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
            return render(request, 'lkp_logic/category_for_checking.html', context)

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
                return redirect('category_for_checking', _id)

        except Exception as e:
            messages.error(request, f'Не удалось сохранить данные. Ошибка: {e}')
            return redirect('category_for_checking', _id)

        messages.success(request, 'Данные успешно сохранены!')
        return redirect('category_for_checking', _id)

    messages.error(request, 'Не определён метод запроса')
    return redirect('home')
