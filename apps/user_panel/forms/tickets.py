from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.translation import gettext_lazy as _

# region add ticket message
from apps.admin_panel.models import Ticket


class AddTicketMessageForm(forms.Form):
    text = forms.CharField(
        label=_('Ticket message'),
        widget=CKEditorWidget(config_name='user_side')
    )


# endregion

# region add ticket

class AddNewTicketForm(forms.Form):
    title = forms.CharField(
        label=_('Title'),
        widget=forms.TextInput(
            attrs={'class': 'form-control'},
        )
    )

    priority = forms.ChoiceField(
        label=_('Priority'),
        initial=Ticket.TicketPriority.MEDIUM,
        choices=Ticket.TicketPriority.choices,
        help_text=_('Priority'),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    section = forms.ChoiceField(
        label=_('Ticket section'),
        initial=Ticket.TicketSection.TECHNICAL,
        choices=Ticket.TicketSection.choices,
        help_text=_('Ticket section'),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    text = forms.CharField(
        label=_('Ticket message'),
        widget=CKEditorWidget(config_name='user_side')
    )

# endregion
