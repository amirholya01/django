from django import forms
from django.utils.translation import gettext_lazy as _


class ChargeWalletForm(forms.Form):
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off',
            'placeholder': _('Toman')
        }),
        label=_('Price'),
    )
