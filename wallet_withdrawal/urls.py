from wallet_withdrawal import views
from django.urls import path

urlpatterns = [

    # ! [withdrawal]
    path('', views.Withdrawal_All.as_view()),
    path('create/', views.Withdrawal_Create.as_view()),
    path('accept/<str:id>/', views.Withdrawal_Accept.as_view()),
    path('reject/<str:id>/', views.Withdrawal_Reject.as_view()),
    # * Update - Retrieve
    path('<str:id>/', views.Withdrawal_UR.as_view()),

]
