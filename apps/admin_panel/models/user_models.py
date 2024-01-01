from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


# region user

class CustomUserManager(UserManager):
    def get_user_by_email(self, email: str):
        return self.get_queryset().filter(email__iexact=email).first()

    def is_exists_user_by_email(self, email: str):
        return self.get_queryset().filter(email__iexact=email).exists()

    def get_user_by_email_active_code(self, active_code):
        return self.get_queryset().filter(email_active_code__iexact=active_code).first()

    def get_user_for_side_bar(self, user_id: int):
        return self.get_queryset().filter(id=user_id).first()

    def get_user_by_id(self, user_id: int):
        return self.get_queryset().filter(id=user_id).first()


class User(AbstractUser):
    mobile = models.CharField(max_length=200, verbose_name=_('Mobile'), db_index=True, null=True, blank=True)
    avatar = models.ImageField(upload_to='images/user-avatar', max_length=200, null=True, blank=True, verbose_name=_('Avatar'))
    email_active_code = models.CharField(max_length=300, verbose_name=_('Email active code'))
    description = RichTextField(verbose_name=_('Description'), null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return f'{self.first_name} {self.last_name}'
        else:
            return self.email

    def get_user_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return '/static/defaults/images/avatar.png'

    def get_user_default_avatar(self):
        return '/static/defaults/images/avatar.png'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

# endregion
