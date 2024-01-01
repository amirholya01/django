from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _


# region ticket

class TicketManager(models.Manager):
    def get_user_tickets(self, user_id):
        return self.get_queryset().filter(owner_id=user_id)

    def get_ticket_for_show(self, ticket_id, user_id):
        return self.get_queryset().filter(id=ticket_id, owner_id=user_id) \
            .prefetch_related('ticketmessage_set', 'ticketmessage_set__sender').first()

    def is_ticket_for_user(self, ticket_id, user_id) -> bool:
        return self.get_queryset().filter(id=ticket_id, owner_id=user_id).exists()

    def get_user_tickets_count(self, user_id):
        return self.get_queryset().filter(owner_id=user_id).count()


class Ticket(models.Model):
    class TicketSection(models.TextChoices):
        SUPPORT = 'SUPPORT', _('Support')
        TECHNICAL = 'Technical', _('Technical')
        FINANCIAL = 'Financial', _('Financial')

    class TicketState(models.TextChoices):
        ANSWERED = 'Answered', _('Answered')
        NOT_ANSWERED = 'NotAnswered', _('Not answered')
        CLOSED = 'Closed', _('Closed')
        UNDER_PROGRESS = 'UnderProgress', _('Under progress')

    class TicketPriority(models.TextChoices):
        LOW = 'Low', _('Low')
        MEDIUM = 'Medium', _('Medium')
        HIGH = 'High', _('High')

    title = models.CharField(max_length=300, verbose_name=_('Title'))
    ticket_section = models.CharField(max_length=300, choices=TicketSection.choices, default=TicketSection.TECHNICAL, verbose_name=_('Ticket section'))
    ticket_state = models.CharField(max_length=300, choices=TicketState.choices, default=TicketState.NOT_ANSWERED, verbose_name=_('Ticket state'))
    ticket_priority = models.CharField(max_length=300, choices=TicketPriority.choices, default=TicketPriority.MEDIUM, verbose_name=_('Priority'))
    owner = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name=_('Owner'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))
    is_delete = models.BooleanField(verbose_name=_('Deleted or not'))

    objects = TicketManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')


# endregion

# region ticket message

class TicketMessageManager(models.Manager):
    def get_ticket_messages_for_show_in_user_panel(self, ticket_id):
        return self.get_queryset().filter(ticket_id=ticket_id, is_delete=False).order_by('-create_date')


class TicketMessage(models.Model):
    sender = models.ForeignKey(to='User', on_delete=models.CASCADE, verbose_name=_('Sender'))
    ticket = models.ForeignKey(to='Ticket', on_delete=models.CASCADE, verbose_name=_('Ticket'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))
    text = RichTextField(verbose_name=_('Text'))
    is_delete = models.BooleanField(verbose_name=_('Deleted or not'))

    objects = TicketMessageManager()

    def __str__(self):
        return f'{self.sender.email} - {self.ticket.title}'

    class Meta:
        verbose_name = _('Ticket message')
        verbose_name_plural = _('Ticket messages')

# endregion
