from django.urls.conf import include
from authentication import views
from django.urls import path

urlpatterns = [

    # * user managment [Admin permission]
    path('admin/users/', views.AllUser.as_view()),
    path('admin/users/<str:id>/', views.GetUser.as_view()),

    # ! type can be { employee , Visitor , customer , Expert }
    path('register/<str:type>/', views.Register.as_view()),

    # ! type can be { admin , employee , Visitor , customer , Expert }
    path('login/username/<str:type>/', views.Login.as_view()),
    path('my_info/<str:type>/', views.MyUserInfo.as_view()),
    path('my_info/update/<str:type>/', views.MyInfoUpdate.as_view()),
    path('logout/<str:type>/', views.Logout.as_view()),
    path('delete_my_account/', views.DeleteAccount.as_view()),

    # ! Address
    path('my/address/<str:user_type>/', views.MyAddress.as_view()),
    path('address/see/', views.AddressSee.as_view()),

    # ! Company
    path('my/company/<str:user_type>/', views.MyCompany.as_view()),
    path('company/see/', views.CompanySee.as_view()),

    # ! Social Media
    path('my/social-media/<str:user_type>/', views.MySocialMedia.as_view()),
    path('social-media/see/', views.SocialMediaSee.as_view()),

    # ! other info
    path('my/info/<str:user_type>/', views.MyInfo.as_view()),
    path('info/see/', views.InfoSee.as_view()),

    # ! session
    path('session/', views.Session.as_view()),
    path('session/see/<str:user_type>/', views.SessionSee.as_view()),

    # ! security Questions
    # * admin :
    path('admin/security/', views.AdminSecurity.as_view()),
    # * user :
    path('user/security-questions/', views.SecurityQuestions.as_view()),
    path('user/security-answer/', views.SecurityAnswer.as_view()),
    path('user/recovery/by-last-password/',
         views.RecoveryByLastPassword.as_view()),
    path('user/recovery/new-password/', views.RecoveryNewPassword.as_view()),

    path('update-token/', views.UpdateToken.as_view()),

]
