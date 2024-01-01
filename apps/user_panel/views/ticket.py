import datetime
from django.contrib import messages
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.list import ListView
from apps.admin_panel.models import Ticket, TicketMessage
from django.utils.translation import gettext_lazy as _
from apps.user_panel.forms.tickets import AddTicketMessageForm, AddNewTicketForm


# region user tickets

@method_decorator(login_required, name='dispatch')
class TicketsView(ListView):
    template_name = 'user_panel/tickets/all_tickets.html'
    model = Ticket
    paginate_by = 6

    def get_queryset(self):
        request: HttpRequest = self.request
        query = Ticket.objects.filter(owner_id=request.user.id, is_delete=False).order_by('-create_date')

        return query


# endregion

# region ticket detail

@method_decorator(login_required, name='dispatch')
class TicketDetailPage(View):
    def get(self, request: HttpRequest, ticket_id: int):
        ticket: Ticket = Ticket.objects.get_ticket_for_show(ticket_id, request.user.id)
        if ticket is None:
            raise Http404(_('Information not found'))
        ticket_messages = TicketMessage.objects.get_ticket_messages_for_show_in_user_panel(ticket.id)
        add_ticket_message_form = AddTicketMessageForm()
        return render(request, 'user_panel/tickets/ticket_detail.html', {
            'ticket': ticket,
            'ticket_messages': ticket_messages,
            'form': add_ticket_message_form
        })

    def post(self, request: HttpRequest, ticket_id: int):
        add_message_form = AddTicketMessageForm(request.POST)
        if add_message_form.is_valid():
            ticket = Ticket.objects.get_ticket_for_show(ticket_id, request.user.id)
            if ticket is not None:
                ticket_message = TicketMessage(
                    ticket_id=ticket_id,
                    sender_id=request.user.id,
                    text=add_message_form.cleaned_data.get('text'),
                    is_delete=False
                )
                ticket_message.save()
                # update ticket itself
                ticket.ticket_state = Ticket.TicketState.UNDER_PROGRESS
                ticket.save()
                messages.add_message(request, messages.SUCCESS, _('Your message has been send successfully'))
            else:
                raise Http404(_('Information not found'))
        else:
            messages.add_message(request, messages.ERROR, _('Please enter message text'))

        return redirect(reverse('ticket_detail_page', kwargs={'ticket_id': ticket_id}))


# endregion

# region add new ticket

class AddNewTicketPage(View):
    def get(self, request: HttpRequest):
        ticket_form = AddNewTicketForm()
        return render(request, 'user_panel/tickets/add_ticket.html', {'form': ticket_form})

    def post(self, request: HttpRequest):
        ticket_form = AddNewTicketForm(request.POST)
        if ticket_form.is_valid():
            new_ticket = Ticket(
                owner_id=request.user.id,
                create_date=datetime.datetime.now(),
                ticket_state=Ticket.TicketState.UNDER_PROGRESS,
                is_delete=False,
                ticket_priority=ticket_form.cleaned_data.get('priority'),
                ticket_section=ticket_form.cleaned_data.get('section'),
                title=ticket_form.cleaned_data.get('title')
            )
            new_ticket.save()
            new_message = TicketMessage(
                ticket_id=new_ticket.id,
                is_delete=False,
                create_date=datetime.datetime.now(),
                sender_id=request.user.id,
                text=ticket_form.cleaned_data.get('text')
            )
            new_message.save()
            messages.add_message(request, messages.SUCCESS, _('Your ticket submitted successfully'))
            return redirect(reverse('tickets_page'))
        return render(request, 'user_panel/tickets/add_ticket.html', {'form': ticket_form})

# endregion
