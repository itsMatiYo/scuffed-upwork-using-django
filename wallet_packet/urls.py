from wallet_packet import views
from django.urls import include, path

urlpatterns = [

    # ! [packet]
    # * All packet obj
    path('', views.Packet_All.as_view()),
    # * Update and Retrieve obj
    path('<str:id>/', views.Packet_UR.as_view()),

]
