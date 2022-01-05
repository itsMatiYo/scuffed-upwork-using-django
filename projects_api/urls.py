from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from . import views
from .views import StartChatBetweenExpertAndEmployees

router = DefaultRouter()
router.register('admin/verifyexpert', views.VerifyExpertViewSet)

urlpatterns = [
    path('<int:pk>/', views.ProjectDetail.as_view()),
    path('', views.ProjectList.as_view()),


    path('<int:project_id>/pre_price/',
         views.PrpjectPrePrice.as_view()),

    # ! employee A/R [result --> accept or reject ]
    path('employee/<int:project_id>/do/<str:result>/',
         views.EmployeeProjectDo.as_view()),
    # ! visitor A/R [result --> accept or reject ]
    path('visitor/<int:project_id>/do/<str:result>/',
         views.VisitorProjectDo.as_view()),

    path('verifyexpert/<pk>/', views.VerifyExpertAPI.as_view()),
    path('<pk>/verifyexperts/', views.ListProjectVerifyExpert.as_view()),
    path('verifyexperts/', views.ListVerifyExperts.as_view()),

    path('paydate/', views.PayDateTimeList.as_view()),
    path('paydate/<int:pk>/', views.PayDateTimeDetail.as_view()),
    path('paydate/pay/<int:pk>/', views.PayDateTimePay.as_view()),

    path('<int:project_id>/return_mony/',
         views.ReMoney.as_view()),

    path('part/city_admin/', views.PartCityAdmin.as_view()),
    path('part/city_admin/<str:id>/', views.PartCityAdmin.as_view()),
    path('part/customer/', views.PartCustomer.as_view()),

    # EmployeeCount Views
    path('empcount/', views.EmpCountList.as_view()),
    path('empcount/<int:pk>/', views.EmpCountDetail.as_view()),

    path('<int:pk>/chat/expertandemployees/',
         StartChatBetweenExpertAndEmployees.as_view()),


    #  router urls
    path('', include(router.urls))

]
