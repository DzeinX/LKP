from django.contrib import admin
from .models import *


admin.site.register(Department)
admin.site.register(Position)
admin.site.register(FileCategory)
admin.site.register(Inspector)


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    fields = [
        'value',
        'lock',
        'comment',
        'visible',
        'field',
        'user',
        'category',
    ]

    raw_id_fields = ['field', 'user', 'category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'start_filling',
        'end_filling',
        'start_checking',
        'end_checking',
    ]


@admin.register(ReportingPeriod)
class ReportingPeriodAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'start',
        'end',
    ]


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'commentable',
        'reporting_period',
    ]

    raw_id_fields = ['reporting_period', ]


@admin.register(FormPosition)
class FormPositionAdmin(admin.ModelAdmin):
    fields = [
        'form',
        'position',
    ]

    raw_id_fields = ['form', 'position', ]


@admin.register(FormCategory)
class FormCategoryAdmin(admin.ModelAdmin):
    fields = [
        'form',
        'category',
    ]

    raw_id_fields = ['form', 'category', ]


@admin.register(FormReportingPeriod)
class FormReportingPeriodAdmin(admin.ModelAdmin):
    fields = [
        'form',
        'reporting_period',
    ]

    raw_id_fields = ['form', 'reporting_period', ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = [
        'username',
        'password',
        'full_name',
        'is_active',
        'objectguid',
        'avatar',
        'orcid',
        'wosrid',
        'said',
        'spin',
        'inspector',
        'department',
        'position',
        'is_superuser',
        'is_staff',
        'first_name',
        'last_name',
        'email',
    ]

    raw_id_fields = ['inspector', 'department', 'position', ]


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'role',
    ]

    raw_id_fields = ['user', 'role', ]


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    fields = [
        'index',
        'name',
        'description',
        'form',
        'inspector',
    ]

    raw_id_fields = ['form', 'inspector', ]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'display_name',
    ]


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'description',
        'file_category',
        'user',
    ]

    raw_id_fields = ['file_category', 'user', ]
