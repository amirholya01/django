from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# region login form

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        }),
        label=_('Email'),
        validators=[
            validators.EmailValidator(_('Email address is not valid')),
            validators.MaxLengthValidator(150, _('This field can not have more than 150 characters')),
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


# endregion

# region register form

class RegisterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        }),
        label=_('Email'),
        validators=[
            validators.EmailValidator(_('Email address is not valid')),
            validators.MaxLengthValidator(150, _('This field can not have more than 150 characters')),
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

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if confirm_password != password:
            raise ValidationError(_('Password and confirm password does not match'), code='password_unmatch')

        return confirm_password


# endregion

# region forgot password

class ForgotPassword(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        }),
        label=_('Email'),
        validators=[
            validators.EmailValidator(_('Email address is not valid')),
            validators.MaxLengthValidator(150, _('This field can not have more than 150 characters')),
        ]
    )


# endregion

# region reset password

class ResetPasswordForm(forms.Form):
    email_active_code = forms.CharField(
        widget=forms.HiddenInput(),
        label=_('Email active code')
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

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if confirm_password != password:
            raise ValidationError(_('Password and confirm password does not match'), code='password_unmatch')

        return confirm_password

# endregion
