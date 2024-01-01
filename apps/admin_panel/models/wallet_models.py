from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from utilities.convertors import date_convertor


# region user wallet

class UserWalletManager(models.Manager):
    def charge_user_wallet(self, user_id, price, user_ip):
        wallet = UserWallet(user_id=user_id, price=price, user_ip=user_ip, transaction_for=UserWallet.TransactionFor.CHARGE, transaction_type=UserWallet.TransactionType.DEPOSIT, transaction_way=UserWallet.TransactionWay.ONLINE)
        wallet.save()

    def get_user_paid_transactions_count(self, user_id):
        return self.get_queryset().filter(is_paid=True, user_id=user_id).count()

    def filter_wallets(self, **kwargs):
        query = self.get_queryset()
        transaction_for_list = kwargs.get('transaction_for_list')
        transaction_way_list = kwargs.get('transaction_way_list')
        transaction_type_list = kwargs.get('transaction_type_list')
        user_id = kwargs.get('user_id')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        tracking_code = kwargs.get('tracking_code')
        is_paid_check_list = kwargs.get('is_paid_check_list')
        lang = get_language()
        if lang == 'fa':
            start_date = date_convertor.convert_shamsi_to_miladi(start_date)
            end_date = date_convertor.convert_shamsi_to_miladi(end_date)

        if transaction_for_list is not None:
            query = query.filter(transaction_way__in=transaction_way_list)

        if transaction_type_list is not None:
            query = query.filter(transaction_type__in=transaction_type_list)

        if transaction_way_list is not None:
            query = query.filter(transaction_way__in=transaction_way_list)

        if user_id is not None:
            query = query.filter(user_id=user_id)

        if start_date is not None and start_date is not '':
            query = query.filter(payment_date__gte=start_date)

        if end_date is not None and end_date is not '':
            query = query.filter(payment_date__lte=end_date)

        if tracking_code is not None:
            query = query.filter(tracking_code__icontains=tracking_code)

        if is_paid_check_list is not None:
            query = query.filter(is_paid__in=is_paid_check_list)

        return query.distinct(), kwargs


class UserWallet(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = 'DEPOSIT', _('Deposit')
        WITHDRAWAL = 'WITHDRAWAL', _('Withdrawal')

    class TransactionWay(models.TextChoices):
        ONLINE = 'ONLINE', _('Online')
        CASH = 'CASH', _('CASH')
        CHARGE_BY_ADMIN = 'CHARGE_BY_ADMIN', _('Charge by admin')
        CARD_TO_CARD = 'CARD_TO_CARD', _('Card to card')

    class TransactionFor(models.TextChoices):
        DISCOUNT = 'DISCOUNT', _('Discount')
        BUY_COURSE = 'BUY_COURSE', _('Buy course')
        CHARGE = 'CHARGE', _('Charge wallet')
        CHECK_OUT = 'CHECK_OUT', _('Checkout')
        REQUEST_CERTIFICATE = 'REQUEST_CERTIFICATE', _('Request certificate')
        REFUND = 'REFUND', _('Refund')
        CONSULT = 'CONSULT', _('Consult')
        OTHER = 'OTHER', _('Other')

    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name=_('User'))
    price = models.IntegerField(default=0, verbose_name=_('Price'))
    transaction_type = models.CharField(choices=TransactionType.choices, max_length=200, verbose_name=_('Transaction type'))
    transaction_way = models.CharField(choices=TransactionWay.choices, max_length=200, verbose_name=_('Transaction way'))
    transaction_for = models.CharField(choices=TransactionFor.choices, max_length=200, verbose_name=_('Transaction for'))
    is_paid = models.BooleanField(default=False, verbose_name=_('Is paid'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Payment date'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    user_ip = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('User IP'))
    authority = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Authority'))
    tracking_code = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Tracking code'))

    objects = UserWalletManager()

    def __str__(self):
        return f'{self.user} / {self.price}'

    class Meta:
        verbose_name = _('User wallet')
        verbose_name_plural = _('User wallets')

# endregion
