from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Отчетный период
class Otch_period(models.Model):
    name = models.CharField('Наименование', max_length=250)
    activ = models.BooleanField('Активен')

    def __str__(self):
        return f'{self.name}'


# Должность
class Post(models.Model):
    name = models.CharField('Наименование', max_length=250)

    def __str__(self):
        return f'{self.name}'


# Проверяющий
class Inspector(models.Model):
    name = models.CharField('Название', max_length=50)
    short_name = models.CharField('Сокращение', max_length=10)

    def __str__(self):
        return f'{self.name}'


# Пользователь
class User(models.Model):
    post_id = models.ManyToManyField(Post)
    inspector_id = models.ManyToManyField(Inspector)

    def __str__(self):
        return f'{self.id}'


# Категория
class Category(models.Model):
    name = models.CharField('Наименование', max_length=250)
    start = models.DateTimeField('Начало активности')
    end = models.DateTimeField('Конец активности')

    def __str__(self):
        return f'{self.name}'


# Анкета
class Anketa(models.Model):
    post_id = models.ManyToManyField(Post)
    otch_period_id = models.ManyToManyField(Otch_period)
    category_id = models.ManyToManyField(Category)
    name = models.CharField('Наименование', max_length=250)
    comment = models.TextField('Коментируемая')

    def __str__(self):
        return f'{self.name}'


# Критерий
class Criteria(models.Model):
    anketa_id = models.ForeignKey(Anketa, on_delete=models.CASCADE)
    inspector_id = models.ForeignKey(Inspector, on_delete=models.CASCADE)
    id_num = models.IntegerField('Порядковый номер', validators=[MinValueValidator(1), MaxValueValidator(100)])
    name = models.CharField('Наименование', max_length=250)
    descriptions = models.TextField('Описание')

    def __str__(self):
        return f'{self.name}'


# Значение (затычка)
class Meaning(models.Model):
    criteria_id = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField('Наименование', max_length=250)
    comment = models.TextField('Коментарий')
    block = models.BooleanField('Блокировка')

    def __str__(self):
        return f'{self.name}'
