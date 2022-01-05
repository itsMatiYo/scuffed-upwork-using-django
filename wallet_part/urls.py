from wallet_part import views
from django.urls import path

urlpatterns = [

    # ! [part]
    path('', views.Part_All.as_view()),
    # * Update - Delete - Retrieve
    path('<str:id>/', views.Part_UDR.as_view()),

]
