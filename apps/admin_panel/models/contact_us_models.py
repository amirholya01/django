from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


# region contact us

class ContactUsManager(models.Manager):
    pass


class ContactUs(models.Model):
    full_name = models.CharField(max_length=200, verbose_name=_('Fullname'))
    subject = models.CharField(max_length=200, verbose_name=_('Subject'))
    email = models.CharField(max_length=200, verbose_name=_('Email'))
    text = RichTextField(verbose_name=_('Text'))
    answer = RichTextField(null=True, blank=True, verbose_name=_('Answer'))
    is_seen = models.BooleanField(default=False, verbose_name=_('Is seen'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))

    objects = ContactUsManager()

    def __str__(self):
        return f'{self.full_name} / {self.subject}'

    class Meta:
        verbose_name = _('Contact Us')
        verbose_name_plural = _('Contact Uses')

# endregion
