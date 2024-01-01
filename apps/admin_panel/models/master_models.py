from django.db import models
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


# region master

class CourseMasterManager(models.Manager):
    def get_by_master_id(self, master_id):
        return self.get_queryset() \
            .prefetch_related('user') \
            .filter(master_courses__main_master_id=master_id) \
            .annotate(course_count=Count('master_courses')) \
            .first()


class CourseMaster(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name=_('User'))
    show_in_list = models.BooleanField(default=True, verbose_name=_('Show in list'))
    description = RichTextField(null=True, blank=True, verbose_name=_('Description'))
    default_share_percentage = models.IntegerField(default=0, verbose_name=_('Default share percentage'))

    objects = CourseMasterManager()

    def __str__(self):
        return str(self.user)

    def get_master_resume_link(self):
        return '#'

    def show_master_name(self):
        if self.user.first_name is not None:
            return f'{self.user.first_name} {self.user.last_name}'
        else:
            return _('Master')

    class Meta:
        verbose_name = _('Course master')
        verbose_name_plural = _('Course masters')

# endregion
