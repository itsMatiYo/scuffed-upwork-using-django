from django.urls import path, include
from users import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('commissions', views.CommisViewSet)
router.register('cityadmin', views.CityAdminViewSet)
router.register('employees', views.EmployeesViewSet)
router.register('visitors', views.VisitorsViewSet)
router.register('experts', views.ExpertsViewSet)

urlpatterns = [
    # * update + delete + get
    path('<str:type>/resume/', views.UserResume.as_view()),
    path('admin/all_resume/', views.AllResume.as_view()),
    path('admin/check/resume/<int:pk>/',
         views.CheckResume.as_view()),

    path('employee/category/<int:pk>/add/',
         views.AddEmployee2Category.as_view()),
    # router urls
    path('', include(router.urls)),
]
