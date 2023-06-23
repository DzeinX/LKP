# Generated by Django 4.2.2 on 2023-06-20 17:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Anketa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Наименование")),
                ("comment", models.TextField(verbose_name="Коментируемая")),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Наименование")),
                ("start", models.TimeField(verbose_name="Начало активности")),
                ("end", models.TimeField(verbose_name="Конец активности")),
            ],
        ),
        migrations.CreateModel(
            name="Criteria",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "id_num",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="Порядковый номер",
                    ),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Наименование")),
                ("descriptions", models.TextField(verbose_name="Описание")),
                (
                    "anketa_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="application_OETD.anketa",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Inspector",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Название")),
                (
                    "short_name",
                    models.CharField(max_length=10, verbose_name="Сокращение"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Otch_period",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Наименование")),
                ("activ", models.BooleanField(verbose_name="Активен")),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Наименование")),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "inspector_id",
                    models.ManyToManyField(to="application_OETD.inspector"),
                ),
                ("post_id", models.ManyToManyField(to="application_OETD.post")),
            ],
        ),
        migrations.CreateModel(
            name="Meaning",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250, verbose_name="Наименование")),
                ("comment", models.TextField(verbose_name="Коментарий")),
                ("block", models.BooleanField(verbose_name="Блокировка")),
                (
                    "category_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="application_OETD.category",
                    ),
                ),
                (
                    "criteria_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="application_OETD.criteria",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="application_OETD.user",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="criteria",
            name="inspector_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="application_OETD.inspector",
            ),
        ),
        migrations.AddField(
            model_name="anketa",
            name="category_id",
            field=models.ManyToManyField(to="application_OETD.category"),
        ),
        migrations.AddField(
            model_name="anketa",
            name="otch_period_id",
            field=models.ManyToManyField(to="application_OETD.otch_period"),
        ),
        migrations.AddField(
            model_name="anketa",
            name="post_id",
            field=models.ManyToManyField(to="application_OETD.post"),
        ),
    ]
