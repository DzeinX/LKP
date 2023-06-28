from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Отчетный период
class Permissions(models.Model):
    key = models.CharField('Значение', max_length=250)
    table_name = models.CharField('Название таблицы', max_length=250,null=True)
    created_at = models.DateTimeField('Время создание ',blank=True)
    updated_at = models.DateTimeField('Время изменения',blank=True)

    def __str__(self):
        return f'{self.table_name}'


class Departments(models.Model):
    name = models.CharField('Наименование', max_length=250)
    level = models.IntegerField('Уровень', validators=[MinValueValidator(1), MaxValueValidator(100)])
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)

    def __str__(self):
        return f'{self.name}'


class Menus(models.Model):
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)
    name = models.CharField('Наименование', max_length=250)

    def __str__(self):
        return f'{self.name}'


class Menuitems(models.Model):
    menu_id = models.ForeignKey(Menus, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=250)
    url = models.CharField('urls', max_length=250)
    target = models.CharField('Цель', max_length=250)
    icon_class = models.CharField('Класс иконки', max_length=250,null=True)
    color = models.CharField('Цвет', max_length=250,null=True)
    parent_id = models.IntegerField('Родительский id', validators=[MinValueValidator(1), MaxValueValidator(100)],null=True)
    order = models.IntegerField('order', validators=[MinValueValidator(1), MaxValueValidator(100)])
    route = models.CharField('Route', max_length=250,null=True)
    parameters = models.TextField('Параметры',null=True)
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)

    def __str__(self):
        return f'{self.title}'


class Categories(models.Model):
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)
    name = models.CharField('Наименование', max_length=250)
    start = models.DateField('Начало активности')
    end = models.DateField('Конец активности')

    def __str__(self):
        return f'{self.name}'


class ReportingPeriods(models.Model):
    name = models.CharField('Наименование', max_length=250)
    active = models.BooleanField('Активная')
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)

    def __str__(self):
        return f'{self.name}'


class Inspectors(models.Model):
    name = models.CharField('Наименование', max_length=250)

    def __str__(self):
        return f'{self.name}'


class Fields(models.Model):
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)
    index = models.CharField('Индекс', max_length=250)
    name = models.TextField('Наименование', max_length=250)
    description = models.TextField('Описание', max_length=250)
    form_id = models.IntegerField("Форма", validators=[MinValueValidator(1), MaxValueValidator(100)])
    inspector_id = models.ForeignKey(Inspectors, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f'{self.name}'


class Forms(models.Model):
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)
    reporting_period_id = models.ForeignKey(ReportingPeriods, on_delete=models.SET_NULL,null=True)
    name = models.CharField('Наименование', max_length=250)
    # не знаю как называть
    commentable = models.IntegerField('commentable')


    def __str__(self):
        return f'{self.name}'


class Roles(models.Model):
    name = models.CharField('Наименование', max_length=250)
    display_name = models.CharField('Название дисплея', max_length=250)
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)

    def __str__(self):
        return f'{self.name}'


class PermissionRole(models.Model):
    permission_id = models.ForeignKey(Permissions, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.permission_id}'


class Positions(models.Model):
    name = models.CharField('Наименование', max_length=250)
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)

    def __str__(self):
        return f'{self.name}'


class FilesCatigories(models.Model):
    name = models.CharField('Наименование', max_length=250)

    def __str__(self):
        return f'{self.name}'


class FormCategory(models.Model):
    form_id = models.ForeignKey(Forms, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.form_id}'


class FormPosition(models.Model):
    position_id = models.ForeignKey(Positions, on_delete=models.CASCADE)
    form_id = models.ForeignKey(Forms, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.form_id}'


class FormReportingPeriod(models.Model):
    reporting_period_id = models.ForeignKey(ReportingPeriods, on_delete=models.CASCADE)
    form_id = models.ForeignKey(Forms, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.form_id}'


class Translations(models.Model):
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)
    table_name = models.CharField("Название", max_length=250)
    column_name = models.CharField("Название столбцов ", max_length=250)
    foreign_key = models.IntegerField('Связь', validators=[MinValueValidator(1), MaxValueValidator(100)])
    locale = models.CharField('Локация', max_length=250)
    value = models.TextField('Значение')

    def __str__(self):
        return f'{self.table_name}'


class Users(models.Model):
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)
    objectguid = models.CharField("objectguid", max_length=250,null=True)
    name = models.CharField("Наименование", max_length=250)
    avatar = models.CharField("avatar", max_length=250,null=True)
    position_id = models.ForeignKey(Positions, on_delete=models.SET_NULL,null=True)
    password = models.CharField("Пароль", max_length=250)
    remember_token = models.IntegerField("remember_token")
    settings = models.TextField("Настройки",null=True)
    username = models.CharField("Имя пользователя", max_length=250)
    inspector_id = models.ForeignKey(Inspectors,on_delete=models.SET_NULL,null=True)
    department_id = models.ForeignKey(Departments, on_delete=models.SET_NULL,null=True)
    orcid = models.CharField("orcid", max_length=250,null=True)
    worsrid = models.CharField("worsrid", max_length=250,null=True)
    said = models.CharField("Оценка", max_length=250,null=True)
    spin = models.CharField('spin', max_length=250,null=True)

    def __str__(self):
        return f'{self.name}'


class UserRoles(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id}'


class Values(models.Model):
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)
    field_id = models.ForeignKey(Fields, on_delete=models.SET_NULL,null=True)
    user_id = models.ForeignKey(Users, on_delete=models.SET_NULL,null=True)
    value = models.TextField("Значение",null=True)
    lock = models.BooleanField("Допуск")
    comment = models.TextField("Комментарий",null=True)
    visible = models.BooleanField("Видимый")
    category_id = models.ForeignKey(Categories,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f'{self.user_id}'


class Files(models.Model):
    created_at = models.DateTimeField('Время создание ', blank=True)
    updated_at = models.DateTimeField('Время изменения', blank=True)
    path = models.CharField('Путь', max_length=250)
    name = models.TextField('Наименование', max_length=250)
    description = models.TextField('Описание', max_length=250)
    file_category_id = models.ForeignKey(FilesCatigories, on_delete=models.SET_NULL,null=True)
    user_id = models.ForeignKey(Users, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f'{self.name}'
