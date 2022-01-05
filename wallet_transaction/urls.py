from wallet_transaction import views
from django.urls import path

urlpatterns = [

    # ! [transaction]
    path('', views.Transaction_All.as_view()),
    path('<str:id>/', views.Transaction_Get_One.as_view()),

    # ! [transaction] all objects in action --> [need-action , holds , accepted , rejected , unpaied-taxes]
    path('all/<str:action>/',
         views.Transaction_Action_Get_All.as_view()),

    # ! [transaction] Do action
    path('<str:id>/hold/',
         views.Transaction_Hold.as_view()),
    path('<str:id>/reject/',
         views.Transaction_Reject.as_view()),
    path('<str:id>/tax/',
         views.Transaction_Tax.as_view()),

    # ! commission ---> [true or false]
    path('<str:id>/accept/<str:commission>/',
         views.Transaction_Accept.as_view()),

]
