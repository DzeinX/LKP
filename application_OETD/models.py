import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from Config import ModelLists

roles = ModelLists.positions


class Positions(models.Model):
    name = models.CharField(max_length=250, null=False)



# Отчетный период
class Permissions(models.Model):
    key = models.CharField('Значение', max_length=250)
    table_name = models.CharField('Название таблицы', max_length=250, null=True)

    created_at = models.DateTimeField('Время создание ', null=True)
    updated_at = models.DateTimeField('Время изменения', null=True)

    def __str__(self):
        return f'{self.table_name}'


class Departments(models.Model):
    name = models.CharField('Наименование', max_length=250)
    level = models.IntegerField('Уровень', validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return f'{self.name}'


# TODO: Сомневаюсь, что эта модель нам нужна, возможно удалим
class Menus(models.Model):
    created_at = models.DateTimeField('Время создание ', null=True)
    updated_at = models.DateTimeField('Время изменения', null=True)
    name = models.CharField('Наименование', max_length=250)

    def __str__(self):
        return f'{self.name}'


# TODO: Сомневаюсь, что эта модель нам нужна, возможно удалим
class MenuItems(models.Model):
    title = models.CharField('Заголовок', max_length=250)
    url = models.CharField('urls', max_length=250)
    target = models.CharField('Цель', max_length=250)
    icon_class = models.CharField('Класс иконки', max_length=250, null=True)
    color = models.CharField('Цвет', max_length=250, null=True)
    parent_id = models.IntegerField('Родительский id', validators=[MinValueValidator(1), MaxValueValidator(100)], null=True)
    order = models.IntegerField('order', validators=[MinValueValidator(1), MaxValueValidator(100)])
    route = models.CharField('Route', max_length=250, null=True)
    parameters = models.TextField('Параметры', null=True)
    created_at = models.DateTimeField('Время создание ', null=True)
    updated_at = models.DateTimeField('Время изменения', null=True)

    menu = models.ForeignKey(Menus, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class Categories(models.Model):
    name = models.CharField('Наименование', max_length=250)
    start = models.DateField('Начало активности')
    end = models.DateField('Конец активности')

    def __str__(self):
        return f'{self.name}'

    def was_active(self):
        date_now = datetime.datetime.now().date()
        if self.start >= date_now and self.end <= date_now:
            return True
        else:
            return False


class ReportingPeriods(models.Model):
    name = models.CharField('Наименование', max_length=250)
    active = models.BooleanField('Активная')
    created_at = models.DateTimeField('Время создание ', null=True)
    updated_at = models.DateTimeField('Время изменения', null=True)

    def __str__(self):
        return f'{self.name}'


class Inspectors(models.Model):
    name = models.CharField('Наименование', max_length=250)

    def __str__(self):
        return f'{self.name}'


class Forms(models.Model):
    created_at = models.DateTimeField('Время создание ', null=True)
    updated_at = models.DateTimeField('Время изменения', null=True)
    name = models.CharField('Наименование', max_length=250)
    commentable = models.CharField('Описание', null=True, max_length=512)

    reporting_period = models.ForeignKey(ReportingPeriods, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f'{self.name}'


class Fields(models.Model):
    created_at = models.DateTimeField('Время создание ', null=True)
    updated_at = models.DateTimeField('Время изменения', null=True)
    index = models.CharField('Индекс', max_length=250)
    name = models.TextField('Наименование', max_length=250)
    description = models.TextField('Описание', max_length=250)

    form = models.ForeignKey(Forms, on_delete=models.SET_NULL, null=True)
    inspector = models.ForeignKey(Inspectors, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}'


class Roles(models.Model):
    name = models.CharField('Наименование', max_length=250)
    display_name = models.CharField('Название дисплея', max_length=250, choices=roles, default=roles[0][0])
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)

    def __str__(self):
        return f'{self.name}'


class PermissionRole(models.Model):
    permission = models.ForeignKey(Permissions, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.permission_id}'


class FilesCatigories(models.Model):
    name = models.CharField('Наименование', max_length=250)

    def __str__(self):
        return f'{self.name}'


class FormCategory(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.form_id}'


class FormPosition(models.Model):
    position = models.ForeignKey(Positions, on_delete=models.CASCADE)
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.form_id}'


class FormReportingPeriod(models.Model):
    reporting_period = models.ForeignKey(ReportingPeriods, on_delete=models.CASCADE)
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.form_id}'


# TODO: Сомневаюсь, что эта модель нам нужна, возможно удалим
class Translations(models.Model):
    created_at = models.DateTimeField('Время создание ', null=True)
    updated_at = models.DateTimeField('Время изменения', null=True)
    table_name = models.CharField("Название", max_length=250)
    column_name = models.CharField("Название столбцов ", max_length=250)
    foreign_key = models.IntegerField('Связь', validators=[MinValueValidator(1), MaxValueValidator(100)])
    locale = models.CharField('Локация', max_length=250)
    value = models.TextField('Значение')

    def __str__(self):
        return f'{self.table_name}'


class User(AbstractUser):
    password = models.CharField("Пароль", max_length=250)
    username = models.CharField("Имя пользователя", max_length=250, unique=True)
    full_name = models.CharField(max_length=60, null=True)
    is_active = models.BooleanField(default=True)
    objectguid = models.CharField("objectguid", max_length=250, null=True)
    avatar = models.CharField("avatar", max_length=250, null=True)
    orcid = models.CharField("orcid", max_length=250, null=True)
    wosrid = models.CharField("worsrid", max_length=250, null=True)
    said = models.CharField("Оценка", max_length=250, null=True)
    spin = models.CharField('spin', max_length=250, null=True)

    inspector = models.ForeignKey(Inspectors, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Departments, null=True, on_delete=models.SET_NULL)
    position = models.ForeignKey(Positions, null=True, on_delete=models.SET_NULL)

    def __repr__(self):
        return f'<User {self.username}>'

    def __str__(self):
        return f'{self.username}'


class UserRoles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id}'


class Values(models.Model):
    created_at = models.DateTimeField('Время создание ', null=True)
    updated_at = models.DateTimeField('Время изменения', null=True)
    value = models.TextField("Значение", null=True)
    lock = models.BooleanField("Допуск")
    comment = models.TextField("Комментарий", null=True)
    visible = models.BooleanField("Видимый")

    field = models.ForeignKey(Fields, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user}'


class Files(models.Model):
    created_at = models.DateTimeField('Время создание ', null=True)
    updated_at = models.DateTimeField('Время изменения', null=True)
    name = models.TextField('Наименование', max_length=250)
    description = models.TextField('Описание', max_length=250)

    file_category = models.ForeignKey(FilesCatigories, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f'{self.name}'
