# Generated by Django 4.2.2 on 2023-06-28 18:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):


    dependencies = [
        ('application_OETD', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name='Время создание '),
        ),
        migrations.AlterField(
            model_name='categories',
            name='updated_at',
            field=models.DateTimeField(blank=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='fields',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name='Время создание '),
        ),
        migrations.AlterField(
            model_name='fields',
            name='updated_at',
            field=models.DateTimeField(blank=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='files',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name='Время создание '),
        ),
        migrations.AlterField(
            model_name='files',
            name='file_category_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.filescatigories'),
        ),
        migrations.AlterField(
            model_name='files',
            name='updated_at',
            field=models.DateTimeField(blank=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='files',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.users'),
        ),
        migrations.AlterField(
            model_name='forms',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name='Время создание '),
        ),
        migrations.AlterField(
            model_name='forms',
            name='updated_at',
            field=models.DateTimeField(blank=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='menuitems',
            name='color',
            field=models.CharField(max_length=250, null=True, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='menuitems',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name='Время создание '),
        ),
        migrations.AlterField(
            model_name='menuitems',
            name='icon_class',
            field=models.CharField(max_length=250, null=True, verbose_name='Класс иконки'),
        ),
        migrations.AlterField(
            model_name='menuitems',
            name='parameters',
            field=models.TextField(null=True, verbose_name='Параметры'),
        ),
        migrations.AlterField(
            model_name='menuitems',
            name='parent_id',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Родительский id'),
        ),
        migrations.AlterField(
            model_name='menuitems',
            name='route',
            field=models.CharField(max_length=250, null=True, verbose_name='Route'),
        ),
        migrations.AlterField(
            model_name='menuitems',
            name='updated_at',
            field=models.DateTimeField(blank=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='positions',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name='Время создание '),
        ),
        migrations.AlterField(
            model_name='positions',
            name='updated_at',
            field=models.DateTimeField(blank=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='reportingperiods',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name='Время создание '),
        ),
        migrations.AlterField(
            model_name='reportingperiods',
            name='updated_at',
            field=models.DateTimeField(blank=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='roles',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name='Время создание '),
        ),
        migrations.AlterField(
            model_name='roles',
            name='updated_at',
            field=models.DateTimeField(blank=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='translations',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name='Время создание '),
        ),
        migrations.AlterField(
            model_name='translations',
            name='updated_at',
            field=models.DateTimeField(blank=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='users',
            name='avatar',
            field=models.CharField(max_length=250, null=True, verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='users',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name='Время создание '),
        ),
        migrations.AlterField(
            model_name='users',
            name='department_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.departments'),
        ),
        migrations.AlterField(
            model_name='users',
            name='inspector_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.inspectors'),
        ),
        migrations.AlterField(
            model_name='users',
            name='objectguid',
            field=models.CharField(max_length=250, null=True, verbose_name='objectguid'),
        ),
        migrations.AlterField(
            model_name='users',
            name='orcid',
            field=models.CharField(max_length=250, null=True, verbose_name='orcid'),
        ),
        migrations.AlterField(
            model_name='users',
            name='position_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.positions'),
        ),
        migrations.AlterField(
            model_name='users',
            name='said',
            field=models.CharField(max_length=250, null=True, verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='users',
            name='settings',
            field=models.TextField(null=True, verbose_name='Настройки'),
        ),
        migrations.AlterField(
            model_name='users',
            name='spin',
            field=models.CharField(max_length=250, null=True, verbose_name='spin'),
        ),
        migrations.AlterField(
            model_name='users',
            name='updated_at',
            field=models.DateTimeField(blank=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='users',
            name='worsrid',
            field=models.CharField(max_length=250, null=True, verbose_name='worsrid'),
        ),
        migrations.AlterField(
            model_name='values',
            name='category_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.categories'),
        ),
        migrations.AlterField(
            model_name='values',
            name='comment',
            field=models.TextField(null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='values',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name='Время создание '),
        ),
        migrations.AlterField(
            model_name='values',
            name='field_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.fields'),
        ),
        migrations.AlterField(
            model_name='values',
            name='updated_at',
            field=models.DateTimeField(blank=True, verbose_name='Время изменения'),
        ),
        migrations.AlterField(
            model_name='values',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.users'),
        ),
        migrations.AlterField(
            model_name='values',
            name='value',
            field=models.TextField(null=True, verbose_name='Значение'),
        ),
    ]
