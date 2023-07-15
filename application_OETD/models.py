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


class Department(models.Model):
    name = models.CharField('Наименование', max_length=250)
    level = models.IntegerField('Уровень', validators=[MinValueValidator(1), MaxValueValidator(100)])

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"

    def __str__(self):
        return f'{self.name}'


class ReportingPeriod(models.Model):
    name = models.CharField('Наименование', max_length=250)
    start = models.DateField('Начало периода')
    end = models.DateField('Конец периода')

    class Meta:
        verbose_name = "Отчётный период"
        verbose_name_plural = "Отчётные периоды"

    def is_active(self):
        date_now = datetime.datetime.now().date()
        return True if self.start <= date_now <= self.end else False

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField('Наименование', max_length=250)
    start_filling = models.DateField('Начало заполнения')
    end_filling = models.DateField('Конец заполнения')
    start_checking = models.DateField('Начало проверки')
    end_checking = models.DateField('Конец проверки')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse("category_detail", args=[str(self.id)])

    def is_can_filling(self) -> bool:
        date_now = datetime.datetime.now().date()
        return True if self.start_filling <= date_now <= self.end_filling else False

    def is_can_checking(self) -> bool:
        date_now = datetime.datetime.now().date()
        return True if self.start_checking <= date_now <= self.end_checking else False

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
        verbose_name = "Анкета"
        verbose_name_plural = "Анкеты"

    def get_absolute_url(self):
        return reverse("form_details", args=[str(self.id)])

    def get_current_filling_period(self) -> Category or None:
        form_categories = FormCategory.objects.filter(form_id=self.id).all()
        for form_category in form_categories:
            category = Category.objects.get(id=form_category.category_id)
            if category.is_can_filling():
                return category
        return None

    def get_current_checking_period(self) -> Category or None:
        form_categories = FormCategory.objects.filter(form_id=self.id).all()
        for form_category in form_categories:
            category = Category.objects.get(id=form_category.category_id)
            if category.is_can_checking():
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
        verbose_name = "Поле анкеты"
        verbose_name_plural = "Поля анкет"

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
        verbose_name = "Анкета & Категория"
        verbose_name_plural = "Анкеты & Категории"

    def __str__(self):
        return f'{self.form.name} & {self.category.name}'


class FormPosition(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Анкета & Должность"
        verbose_name_plural = "Анкеты & Должности"

    def __str__(self):
        return f'{self.form.name} & {self.position.name}'


class FormReportingPeriod(models.Model):
    reporting_period = models.ForeignKey(ReportingPeriod, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Анкета & Отчётный период"
        verbose_name_plural = "Анкеты & Отчётные периоды"

    def __str__(self):
        return f'{self.form.name} & {self.reporting_period.name}'


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
