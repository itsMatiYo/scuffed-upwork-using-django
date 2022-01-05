from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from it.utils import update_roles

urlpatterns = [
    path('admin/', admin.site.urls),
    # * Authentication
    path('auth/', include('authentication.urls')),
    # * Wallet
    path('wallet/', include('wallet.urls')),
    path('creditcard/', include('wallet_creditcard.urls')),
    path('locked/', include('wallet_locked.urls')),
    path('packet/', include('wallet_packet.urls')),
    path('part/', include('wallet_part.urls')),
    path('payment/', include('wallet_payment.urls')),
    path('transaction/', include('wallet_transaction.urls')),
    path('withdrawal/', include('wallet_withdrawal.urls')),

    path('users/', include("users.urls")),

    path('projects/', include('projects_api.urls')),
    path('', include('itapi.urls')),

    path('mail/', include('mail.urls')),
]

# update_roles()
