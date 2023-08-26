from django.contrib import admin
from user.models import User, OtpCode, Subscription
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.forms import UserCreationForm, UserChangeForm


admin.site.register(Subscription)


class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'created_at')


admin.site.register(OtpCode, OtpCodeAdmin)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'phone_number', 'id')
    list_filter = ('is_superuser',)

    fieldsets = (
        ('personal information', {'fields': ('email', 'first_name', 'phone_number', 'password', 'last_login')}),
        ('permissions', {'fields': ('is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        ('personal information', {'fields': ('email', 'first_name', 'phone_number', 'password', 'last_login')}),
        ('permissions', {'fields': ('is_superuser', 'groups', 'user_permissions')}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)
