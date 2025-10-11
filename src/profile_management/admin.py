from django.contrib import admin

from .models import NewUser


@admin.register(NewUser)
class NewUserAdmin(admin.ModelAdmin):
    fields = (
        "last_name",
        "first_name",
        "patronymic",
        "username",
        "photo",
        "email",
        "groups",
        "is_staff",
        "is_active",
        "date_joined",
        "last_login",
    )
    list_display = ("username", "last_name", "first_name", "patronymic")
    readonly_fields = ("date_joined", "last_login")
