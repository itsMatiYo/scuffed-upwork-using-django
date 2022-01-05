from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('province', views.ProvinceViewSet)
router.register('city', views.CityViewSet)
router.register('timetable', views.TimeTableViewSet)
# router.register('time_table_visitor', views.TimeTableVisitorViewSet)
router.register('report', views.ReportEmployeeViewSet)
router.register('info', views.CompanyInfoViewSet)

urlpatterns = [

    path('category/<int:pk>/', views.CategoryDetail.as_view()),
    path('category/', views.CategoryList.as_view()),
    # router urls
    path('timetablevisitor/', views.TimeTableVisitorList.as_view()),
    path('timetablevisitor/<int:pk>/', views.TimeTableVisitorDetail.as_view()),
    path('', include(router.urls)),
]
