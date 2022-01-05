from wallet import views
from django.urls import include, path

urlpatterns = [

    # ! [wallet]
    # * All wallet obj
    path('', views.Wallet_All.as_view()),
    # * Update and Retrieve obj
    path('<str:id>/', views.Wallet.as_view()),

]
