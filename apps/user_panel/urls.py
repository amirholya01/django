from django.urls import path
from .views import account, ticket, wallet

urlpatterns = [
    # dashboard
    path('', account.UserDashboardPage.as_view(), name='user_dashboard_page'),
    # account
    path('change-pass/', account.ChangePasswordPage.as_view(), name='change_pass_page'),
    path('change-info/', account.ChangeUserInfoPage.as_view(), name='change_user_info_page'),
    # ticket
    path('tickets/', ticket.TicketsView.as_view(), name='tickets_page'),
    path('tickets/add-ticket', ticket.AddNewTicketPage.as_view(), name='add_new_ticket_page'),
    path('tickets/<int:ticket_id>', ticket.TicketDetailPage.as_view(), name='ticket_detail_page'),
    # wallet
    path('my-wallet/', wallet.UserWalletListView.as_view(), name='user_wallets_page'),
    path('charge-wallet/', wallet.ChargeWalletView.as_view(), name='user_charge_wallet_page'),
]
