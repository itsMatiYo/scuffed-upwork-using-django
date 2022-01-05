import asynchat

from django.urls import path

from mail.views import SendFriendRequest, GetFriendRequest, GetFriendRequests, ChangeUserTemporaryLink, ChangeUserLink, \
    Block, Chat, MyChats, ChatBlockUser, JoinChat, ChangeTemporaryLink, ChangeLink, LeaveChat, GetAllReportReasons, \
    SearchMessage, CreateReport, ChatMessages, Message, BannerTimeTable, BannerTimeTables, Banner, GetAllBanners

urlpatterns = [
    path('user/<slug>/friendrequest/', SendFriendRequest.as_view()),
    path('friendrequest/<int:pk>/', GetFriendRequest.as_view()),
    path('friendrequests/', GetFriendRequests.as_view()),
    path('user/temporarylink/change/', ChangeUserTemporaryLink.as_view()),
    path('user/link/change/', ChangeUserLink.as_view()),
    path('block/', Block.as_view()),

    path('chat/', Chat.as_view()),
    path('chat/<int:pk>/', Chat.as_view()),
    path('chat/mine/', MyChats.as_view()),
    path('chat/<int:pk>/block/', ChatBlockUser.as_view()),
    path('chat/<int:pk>/admin/', ChatBlockUser.as_view()),
    path('join/<slug>/', JoinChat.as_view()),
    path('chat/<int:pk>/reset/temporary/', ChangeTemporaryLink.as_view()),
    path('chat/<int:pk>/reset/slug/', ChangeLink.as_view()),
    path('chat/<int:pk>/exit/', LeaveChat.as_view()),
    path('chat/<int:pk>/exit/', LeaveChat.as_view()),
    path('message/search/', SearchMessage.as_view()),
    path('reportreasons/', GetAllReportReasons.as_view()),
    path('reportreason/<int:pk>/', GetAllReportReasons.as_view()),
    path('report/', CreateReport.as_view()),
    path('chat/<int:pk>/messages/', ChatMessages.as_view()),
    path('message/<int:pk>/', Message.as_view()),
    path('message/chat/<int:pk>/', Message.as_view()),

    path('timetable/<int:pk>/', BannerTimeTable.as_view()),
    path('timetables/', BannerTimeTables.as_view()),
    path('banner/', Banner.as_view()),
    path('banner/<int:pk>/', Banner.as_view()),
    path('banners/', GetAllBanners.as_view()),
]