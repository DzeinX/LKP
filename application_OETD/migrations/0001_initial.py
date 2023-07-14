


# Generated by Django 4.2.2 on 2023-07-12 08:56


from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [


        ('auth', '0012_alter_user_first_name_max_length'),

    ]

    operations = [
        migrations.CreateModel(

            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('password', models.CharField(max_length=250, verbose_name='Пароль')),
                ('username', models.CharField(max_length=250, unique=True, verbose_name='Имя пользователя')),
                ('full_name', models.CharField(max_length=60, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('objectguid', models.CharField(blank=True, max_length=250, null=True, verbose_name='objectguid')),
                ('avatar', models.CharField(blank=True, max_length=250, null=True, verbose_name='avatar')),
                ('orcid', models.CharField(blank=True, max_length=250, null=True, verbose_name='orcid')),
                ('wosrid', models.CharField(blank=True, max_length=250, null=True, verbose_name='worsrid')),
                ('said', models.CharField(blank=True, max_length=250, null=True, verbose_name='Оценка')),
                ('spin', models.CharField(blank=True, max_length=250, null=True, verbose_name='spin')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('start', models.DateField(verbose_name='Начало активности')),
                ('end', models.DateField(verbose_name='Конец активности')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('level', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Уровень')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Время создание ')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Время изменения')),
                ('index', models.CharField(max_length=250, verbose_name='Индекс')),
                ('name', models.TextField(max_length=250, verbose_name='Наименование')),
                ('description', models.TextField(max_length=250, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Поле показателя эффективности',
                'verbose_name_plural': 'Поля показателей эффективности',
            },
        ),
        migrations.CreateModel(
            name='FileCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Категория файла',
                'verbose_name_plural': 'Категории файлов',
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Время создание ')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Время изменения')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('commentable', models.CharField(max_length=512, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Показатель эффективности',
                'verbose_name_plural': 'Показатели эффективности',
            },
        ),
        migrations.CreateModel(
            name='Inspector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Проверяющий',
                'verbose_name_plural': 'Проверяющие',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Время создание ')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Время изменения')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=250, verbose_name='Значение')),
                ('table_name', models.CharField(max_length=250, null=True, verbose_name='Название таблицы')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Время создание ')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Время изменения')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
            },
        ),
        migrations.CreateModel(
            name='ReportingPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('active', models.BooleanField(default=True, verbose_name='Активная')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Время создание ')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Время изменения')),
            ],
            options={
                'verbose_name': 'Отчётный период',
                'verbose_name_plural': 'Отчётные периоды',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('display_name', models.CharField(max_length=250, verbose_name='Отображаемое имя')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Время создание ')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Время изменения')),
            ],
            options={
                'verbose_name': 'Роль',
                'verbose_name_plural': 'Роли',
            },
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Время создание ')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Время изменения')),
                ('table_name', models.CharField(max_length=250, verbose_name='Название')),
                ('column_name', models.CharField(max_length=250, verbose_name='Название столбцов ')),
                ('foreign_key', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Связь')),
                ('locale', models.CharField(max_length=250, verbose_name='Локация')),
                ('value', models.TextField(verbose_name='Значение')),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Время создание ')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Время изменения')),
                ('value', models.TextField(null=True, verbose_name='Значение')),
                ('lock', models.BooleanField(verbose_name='Допуск')),
                ('comment', models.TextField(null=True, verbose_name='Комментарий')),
                ('visible', models.BooleanField(default=True, verbose_name='Видимый')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.category')),
                ('field', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.field')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Значение пользователя',
                'verbose_name_plural': 'Значения пользователей',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_OETD.role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пользователь & Роль',
                'verbose_name_plural': 'Пользователи & Роли',
            },
        ),
        migrations.CreateModel(
            name='PermissionRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_OETD.permission')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_OETD.role')),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('url', models.CharField(max_length=250, verbose_name='urls')),
                ('target', models.CharField(max_length=250, verbose_name='Цель')),
                ('icon_class', models.CharField(max_length=250, null=True, verbose_name='Класс иконки')),
                ('color', models.CharField(max_length=250, null=True, verbose_name='Цвет')),
                ('parent_id', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Родительский id')),
                ('order', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='order')),
                ('route', models.CharField(max_length=250, null=True, verbose_name='Route')),
                ('parameters', models.TextField(null=True, verbose_name='Параметры')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Время создание ')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Время изменения')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_OETD.menu')),
            ],
        ),
        migrations.CreateModel(
            name='FormReportingPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_OETD.form')),
                ('reporting_period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_OETD.reportingperiod')),

            ],
            options={
                'verbose_name': 'Показатель эффективности & Отчётный период',
                'verbose_name_plural': 'Показатели эффективности & Отчётные периоды',
            },
        ),
        migrations.CreateModel(
            name='FormPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_OETD.form')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_OETD.position')),
            ],
            options={
                'verbose_name': 'Показатель эффективности & Должность',
                'verbose_name_plural': 'Показатели эффективности & Должности',
            },
        ),
        migrations.CreateModel(
            name='FormCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_OETD.category')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_OETD.form')),
            ],
            options={
                'verbose_name': 'Показатель эффективности & Категория',
                'verbose_name_plural': 'Показатели эффективности & Категории',
            },
        ),
        migrations.AddField(


            model_name='form',
            name='reporting_period',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.reportingperiod'),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Время создание ')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Время изменения')),
                ('name', models.TextField(max_length=250, verbose_name='Наименование')),
                ('description', models.TextField(max_length=250, verbose_name='Описание')),
                ('file_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.filecategory')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.AddField(
            model_name='field',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.form'),
        ),
        migrations.AddField(
            model_name='field',
            name='inspector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.inspector'),
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.department'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='inspector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.inspector'),
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='application_OETD.position'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),

        ),
    ]
