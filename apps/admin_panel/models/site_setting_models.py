from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import Prefetch
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# region site setting

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name=_('Site name'))
    domain_name = models.CharField(max_length=200, verbose_name=_('Domain name'))
    tell = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Phone number'))
    mobile = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Mobile'))
    support_email = models.EmailField(max_length=200, null=True, blank=True, verbose_name=_('Support email'))
    address = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Address'))
    about_us_text = RichTextField(null=True, blank=True, verbose_name=_('About us text'))
    copy_right = models.TextField(null=True, blank=True, verbose_name=_('Copy right'))
    site_header_logo = models.ImageField(upload_to='images/site-logo', null=True, blank=True, verbose_name=_('Header logo'))
    site_footer_logo = models.ImageField(upload_to='images/site-logo', null=True, blank=True, verbose_name=_('Footer logo'))

    class Meta:
        verbose_name = _('Site setting')
        verbose_name_plural = _('Site settings')

    def __str__(self):
        return self.site_name


# endregion

# region links

class DynamicLinksManager(models.Manager):
    def get_active_links_by_position(self, position):
        return self.get_queryset() \
            .filter(is_active=True, is_delete=False, position=position, parent_id__isnull=True).order_by('order') \
            .prefetch_related(
            Prefetch('dynamiclink_set', queryset=DynamicLink.objects.filter(is_active=True, is_delete=False, position=position).prefetch_related(Prefetch('dynamiclink_set', queryset=DynamicLink.objects.filter(is_active=True, is_delete=False, position=position).order_by('order'))).order_by('order'))
        )


class DynamicLink(models.Model):
    class LinkPosition(models.TextChoices):
        SITE_HEADER = 'SITE_HEADER', _('Site header')
        SITE_FOOTER = 'SITE_FOOTER', _('Site footer')

    title = models.CharField(max_length=200, verbose_name=_('Title'))
    url = models.CharField(max_length=200, verbose_name=_('Url'))
    order = models.IntegerField(default=0, verbose_name=_('Order'))
    parent = models.ForeignKey('DynamicLink', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Parent'))
    position = models.CharField(choices=LinkPosition.choices, default=LinkPosition.SITE_HEADER, max_length=200, verbose_name=_('Position'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    is_delete = models.BooleanField(default=False, verbose_name=_('Is deleted'))

    objects = DynamicLinksManager()

    def __str__(self):
        return f'{self.title} / {self.position.title()}'

    class Meta:
        verbose_name = _('Dynamic link')
        verbose_name_plural = _('Dynamic links')


# endregion

# region dynamic page

class DynamicPageManager(models.Manager):
    def get_page_by_url_title(self, url_title):
        return self.get_queryset().filter(url_title__iexact=url_title, is_active=True).first()


class DynamicPage(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    url_title = models.CharField(max_length=200, unique=True, verbose_name=_('Url title'))
    text = RichTextField(verbose_name=_('Text'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))

    objects = DynamicPageManager()

    def __str__(self):
        return f'{self.title} - {self.url_title}'

    def get_url(self):
        return reverse('dynamic_page_view', kwargs={'url_title': self.url_title})

    class Meta:
        verbose_name = _('Dynamic page')
        verbose_name_plural = _('Dynamic pages')

# endregion
