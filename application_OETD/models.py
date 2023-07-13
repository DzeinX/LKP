import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=250, null=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


# TODO: Сомневаюсь, что эта модель нам нужна, возможно удалим
class Permission(models.Model):
    key = models.CharField('Значение', max_length=250)
    table_name = models.CharField('Название таблицы', max_length=250, null=True)

    created_at = models.DateTimeField('Время создание ', null=True, blank=True)
    updated_at = models.DateTimeField('Время изменения', null=True, blank=True)

    def __str__(self):
        return f'{self.table_name}'


class Department(models.Model):
    name = models.CharField('Наименование', max_length=250)
    level = models.IntegerField('Уровень', validators=[MinValueValidator(1), MaxValueValidator(100)])

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    def __str__(self):
        return f'{self.name}'


# TODO: Сомневаюсь, что эта модель нам нужна, возможно удалим
class Menu(models.Model):
    created_at = models.DateTimeField('Время создание ', null=True, blank=True)
    updated_at = models.DateTimeField('Время изменения', null=True, blank=True)
    name = models.CharField('Наименование', max_length=250)

    def __str__(self):
        return f'{self.name}'


# TODO: Сомневаюсь, что эта модель нам нужна, возможно удалим
class MenuItem(models.Model):
    title = models.CharField('Заголовок', max_length=250)
    url = models.CharField('urls', max_length=250)
    target = models.CharField('Цель', max_length=250)
    icon_class = models.CharField('Класс иконки', max_length=250, null=True)
    color = models.CharField('Цвет', max_length=250, null=True)
    parent_id = models.IntegerField('Родительский id', validators=[MinValueValidator(1), MaxValueValidator(100)], null=True)
    order = models.IntegerField('order', validators=[MinValueValidator(1), MaxValueValidator(100)])
    route = models.CharField('Route', max_length=250, null=True)
    parameters = models.TextField('Параметры', null=True)
    created_at = models.DateTimeField('Время создание ', null=True, blank=True)
    updated_at = models.DateTimeField('Время изменения', null=True, blank=True)

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class Category(models.Model):
    name = models.CharField('Наименование', max_length=250)
    start = models.DateField('Начало активности')
    end = models.DateField('Конец активности')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse("category_detail", args=[str(self.id)])

    def was_active(self):
        date_now = datetime.datetime.now().date()
        if self.start <= date_now <= self.end:
            return True
        else:
            return False

    def __str__(self):
        return f'{self.name}'


class ReportingPeriod(models.Model):
    name = models.CharField('Наименование', max_length=250)
    active = models.BooleanField('Активная', default=True)
    created_at = models.DateTimeField('Время создание ', null=True, blank=True)
    updated_at = models.DateTimeField('Время изменения', null=True, blank=True)

    class Meta:
        verbose_name = "Отчётный период"
        verbose_name_plural = "Отчётные периоды"

    def __str__(self):
        return f'{self.name}'


class Inspector(models.Model):
    name = models.CharField('Наименование', max_length=250)

    class Meta:
        verbose_name = "Проверяющий"
        verbose_name_plural = "Проверяющие"

    def __str__(self):
        return f'{self.name}'


class Form(models.Model):
    created_at = models.DateTimeField('Время создание ', null=True, blank=True)
    updated_at = models.DateTimeField('Время изменения', null=True, blank=True)
    name = models.CharField('Наименование', max_length=250)
    commentable = models.CharField('Описание', null=True, max_length=512)

    reporting_period = models.ForeignKey(ReportingPeriod, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Показатель эффективности"
        verbose_name_plural = "Показатели эффективности"

    def get_absolute_url(self):
        return reverse("form_details", args=[str(self.id)])

    def get_current_category(self) -> Category or None:
        form_categories = FormCategory.objects.filter(form_id=self.id).all()
        for form_category in form_categories:
            category = Category.objects.get(id=form_category.category_id)
            if category.was_active():
                return category
        return None

    def __str__(self):
        return f'{self.name}'


class Field(models.Model):
    created_at = models.DateTimeField('Время создание ', null=True, blank=True)
    updated_at = models.DateTimeField('Время изменения', null=True, blank=True)
    index = models.CharField('Индекс', max_length=250)
    name = models.TextField('Наименование', max_length=250)
    description = models.TextField('Описание', max_length=250)

    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True)
    inspector = models.ForeignKey(Inspector, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Поле показателя эффективности"
        verbose_name_plural = "Поля показателей эффективности"

    def get_absolute_url(self):
        return reverse("field_detail", args=[str(self.id)])

    def __str__(self):
        return f'{self.name}'


class Role(models.Model):
    name = models.CharField('Наименование', max_length=250)
    display_name = models.CharField('Отображаемое имя', max_length=250)
    created_at = models.DateTimeField('Время создание ', blank=True, null=True)
    updated_at = models.DateTimeField('Время изменения', blank=True, null=True)

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return f'{self.display_name}'


# TODO: Сомневаюсь, что эта модель нам нужна, возможно удалим
class PermissionRole(models.Model):
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.permission.table_name} & {self.role.name}'


class FileCategory(models.Model):
    name = models.CharField('Наименование', max_length=250)

    class Meta:
        verbose_name = "Категория файла"
        verbose_name_plural = "Категории файлов"

    def __str__(self):
        return f'{self.name}'


class FormCategory(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Показатель эффективности & Категория"
        verbose_name_plural = "Показатели эффективности & Категории"

    def __str__(self):
        return f'{self.form.name} & {self.category.name}'


class FormPosition(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Показатель эффективности & Должность"
        verbose_name_plural = "Показатели эффективности & Должности"

    def __str__(self):
        return f'{self.form.name} & {self.position.name}'


class FormReportingPeriod(models.Model):
    reporting_period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Показатель эффективности & Отчётный период"
        verbose_name_plural = "Показатели эффективности & Отчётные периоды"

    def __str__(self):
        return f'{self.form.name} & {self.reporting_period.name}'


# TODO: Сомневаюсь, что эта модель нам нужна, возможно удалим
class Translation(models.Model):
    created_at = models.DateTimeField('Время создание ', null=True, blank=True)
    updated_at = models.DateTimeField('Время изменения', null=True, blank=True)
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
    objectguid = models.CharField("objectguid", max_length=250, null=True, blank=True)
    avatar = models.CharField("avatar", max_length=250, null=True, blank=True)
    orcid = models.CharField("orcid", max_length=250, null=True, blank=True)
    wosrid = models.CharField("worsrid", max_length=250, null=True, blank=True)
    said = models.CharField("Оценка", max_length=250, null=True, blank=True)
    spin = models.CharField('spin', max_length=250, null=True, blank=True)

    inspector = models.ForeignKey(Inspector, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    position = models.ForeignKey(Position, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def get_absolute_url(self):
        return reverse("user_detail", args=[str(self.id)])

    def __repr__(self):
        return f'<User {self.username}>'

    def __str__(self):
        return f'{self.full_name if self.full_name is not None else self.username}'


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Пользователь & Роль"
        verbose_name_plural = "Пользователи & Роли"

    def __str__(self):
        return f'{self.user_id}'


class Value(models.Model):
    created_at = models.DateTimeField('Время создание ', null=True, blank=True)
    updated_at = models.DateTimeField('Время изменения', null=True, blank=True)
    value = models.TextField("Значение", null=True)
    lock = models.BooleanField("Допуск")
    comment = models.TextField("Комментарий", null=True)
    visible = models.BooleanField("Видимый", default=True)

    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Значение пользователя"
        verbose_name_plural = "Значения пользователей"

    def get_absolute_url(self):
        return reverse("value_detail", args=[str(self.id)])

    def __str__(self):
        return f'{self.user} -> {self.field}({self.value})'


class File(models.Model):
    created_at = models.DateTimeField('Время создание ', null=True, blank=True)
    updated_at = models.DateTimeField('Время изменения', null=True, blank=True)
    name = models.TextField('Наименование', max_length=250)
    description = models.TextField('Описание', max_length=250)

    file_category = models.ForeignKey(FileCategory, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def get_absolute_url(self):
        return reverse("file_detail", args=[str(self.id)])

    def __str__(self):
        return f'{self.name} -> {self.user.username}'
