from django import forms
from django.core import validators
from django.utils.translation import gettext_lazy as _


# region change password


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        label=_('Current password'),
        validators=[
            validators.MaxLengthValidator(150, _('This field can not have more than 150 characters'))
        ]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        label=_('Password'),
        validators=[
            validators.MaxLengthValidator(150, _('This field can not have more than 150 characters'))
        ]
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        label=_('Confirm password'),
        validators=[
            validators.MaxLengthValidator(150, _('This field can not have more than 150 characters'))
        ]
    )


# endregion

# region change user info

class ChangeUserInfoForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label=_('First name'),
        validators=[
            validators.MaxLengthValidator(150, _('This field can not have more than 150 characters'))
        ]
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label=_('Last name'),
        validators=[
            validators.MaxLengthValidator(150, _('This field can not have more than 150 characters'))
        ]
    )


# endregion
