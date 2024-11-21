from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm

class UserCreationFormWithGroups(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta(UserCreationForm.Meta):
        model = User

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationFormWithGroups
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'group'),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        group = form.cleaned_data['group']
        obj.groups.set([group])

admin.site.unregister(User)
admin.site.register(User, UserAdmin)