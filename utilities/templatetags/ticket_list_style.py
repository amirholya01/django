from django import template

from apps.admin_panel.models import Ticket

register = template.Library()


@register.filter(name='show_ticket_state')
def get_ticket_style(value: Ticket.TicketState):
    if value == Ticket.TicketState.ANSWERED:
        return 'hold'
    elif value == Ticket.TicketState.NOT_ANSWERED:
        return 'pending'
    elif value == Ticket.TicketState.UNDER_PROGRESS:
        return 'inprogress'
    elif value == Ticket.TicketState.CLOSED:
        return 'complete'
