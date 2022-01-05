from wallet_creditcard import views
from django.urls import path

urlpatterns = [

    # ! [creditcard]
    path('create/', views.Creditcard_Create.as_view()),

    # ! [giftcard]
    path('giftcard/create/', views.Giftcard_Create.as_view()),

    # ! [creditcard $ giftcard]
    path('', views.Card_All.as_view()),
    path('<str:id>/', views.Card_One.as_view()),


]
