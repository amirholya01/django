from django import forms
from django.core import validators
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget


# region create contact us


class CreateContactForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control simple'
        }),
        label=_('Fullname'),
        validators=[
            validators.MaxLengthValidator(200, _('This field can not have more than 200 characters')),
        ]
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control simple'
        }),
        label=_('Email'),
        validators=[
            validators.EmailValidator(_('Email address is not valid')),
            validators.MaxLengthValidator(200, _('This field can not have more than 200 characters')),
        ]
    )

    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control simple'
        }),
        label=_('Subject'),
        validators=[
            validators.MaxLengthValidator(200, _('This field can not have more than 200 characters')),
        ]
    )

    text = forms.CharField(
        widget=CKEditorWidget(attrs={
            'class': 'form-control simple'
        }, config_name='user_side'),
        label=_('Text')
    )

# endregion
