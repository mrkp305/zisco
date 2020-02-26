from django import forms
from django.contrib.auth import forms as auth_forms

from zisco.users.models import Customer


class AuthenticationForm(auth_forms.AuthenticationForm):

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
        if not hasattr(user, "profile"):
            raise forms.ValidationError(
                "Access denied"
            )


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "email", "address")
        widgets = {
            "address": forms.Textarea(
                attrs={
                    "rows": 3
                }
            )
        }
