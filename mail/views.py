from decouple import config

from rest_framework.views import APIView

from mail.utils import Request2Mail, RequestWithFile2Mail

MAIL_HOST = config('MAIL_HOST')


class SendFriendRequest(APIView):
    def post(self, request, *args, **kwargs):
        # Send Friend Request
        return Request2Mail(request, f'{MAIL_HOST}/user/{kwargs["slug"]}/friendrequest/')


class GetFriendRequest(APIView):
    def get(self, request, *args, **kwargs):
        # Get A Friend Request
        return Request2Mail(request, f'{MAIL_HOST}/friendrequest/{kwargs["pk"]}/')

    def put(self, request, *args, **kwargs):
        # Verify A Friend Request
        return Request2Mail(request, f'{MAIL_HOST}/friendrequest/{kwargs["pk"]}/')


class GetFriendRequests(APIView):
    def get(self, request, *args, **kwargs):
        # Get All Friend Requests
        return Request2Mail(request, f'{MAIL_HOST}/friendrequests/')


class ChangeUserTemporaryLink(APIView):
    def post(self, request, *args, **kwargs):
        # Change User Temporary Slug
        return Request2Mail(request, f'{MAIL_HOST}/user/temporarylink/change/')


class ChangeUserLink(APIView):
    def post(self, request, *args, **kwargs):
        # Change User Slug
        return Request2Mail(request, f'{MAIL_HOST}/user/link/change/')


class Block(APIView):
    def post(self, request, *args, **kwargs):
        # Block"""
        return Request2Mail(request, f'{MAIL_HOST}/block/')


class Chat(APIView):
    def post(self, request, *args, **kwargs):
        # Create Chat
        return RequestWithFile2Mail(request=request, link=f'{MAIL_HOST}/chat/', fileName='profile')

    def put(self, request, *args, **kwargs):
        # Edit Chat
        return RequestWithFile2Mail(request=request, link=f'{MAIL_HOST}/chat/{kwargs["pk"]}/', fileName='profile')

    def get(self, request, *args, **kwargs):
        # Get Chat
        return Request2Mail(request, f'{MAIL_HOST}/chat/{kwargs["pk"]}/')

    def delete(self, request, *args, **kwargs):
        # Delete Chat
        return Request2Mail(request, f'{MAIL_HOST}/chat/{kwargs["pk"]}/')


class MyChats(APIView):
    def get(self, request, *args, **kwargs):
        # Get My Chats
        return Request2Mail(request, f'{MAIL_HOST}/chat/mine/')


class ChatBlockUser(APIView):
    def post(self, request, *args, **kwargs):
        # Block
        return Request2Mail(request, f'{MAIL_HOST}/chat/{kwargs["pk"]}/admin/')


class JoinChat(APIView):
    def post(self, request, *args, **kwargs):
        # join chat
        return Request2Mail(request, f'{MAIL_HOST}/join/{kwargs["slug"]}/')


class ChangeTemporaryLink(APIView):
    def post(self, request, *args, **kwargs):
        # change temporary link
        return Request2Mail(request, f'{MAIL_HOST}/chat/{kwargs["pk"]}/reset/temporary/')


class SearchMessage(APIView):
    def get(self, request, *args, **kwargs):
        link = f'{MAIL_HOST}/message/search/?'
        if request.GET.get('sender__id'):
            link += f'sender__id={request.GET.get("sender__id")}'
        if request.GET.get('message'):
            link += f'message={request.GET.get("message")}'
        if request.GET.get('chat'):
            link += f'chat={request.GET.get("chat")}'
        return Request2Mail(request, link)


class ChangeLink(APIView):
    def post(self, request, *args, **kwargs):
        # change link
        return Request2Mail(request, f'{MAIL_HOST}/chat/{kwargs["pk"]}/reset/slug/')


class LeaveChat(APIView):
    def post(self, request, *args, **kwargs):
        # leave chat
        return Request2Mail(request, f'{MAIL_HOST}/chat/{kwargs["pk"]}/exit/')


class GetAllReportReasons(APIView):
    def get(self, request, *args, **kwargs):
        # get all report reasons
        return Request2Mail(request, f'{MAIL_HOST}/reportreason/{kwargs["pk"]}/')


class CreateReport(APIView):
    def post(self, request, *args, **kwargs):
        return Request2Mail(request, f'{MAIL_HOST}/report/')


class Message(APIView):

    def post(self, request, *args, **kwargs):
        return RequestWithFile2Mail(request=request, link=f'{MAIL_HOST}/message/chat/{kwargs["pk"]}/', fileName='file')

    def get(self, request, *args, **kwargs):
        return Request2Mail(request, f'{MAIL_HOST}/message/{kwargs["pk"]}/')

    def delete(self, request, *args, **kwargs):
        return Request2Mail(request, f'{MAIL_HOST}/message/{kwargs["pk"]}/')


class ChatMessages(APIView):
    def get(self, request, *args, **kwargs):
        return Request2Mail(request, f'{MAIL_HOST}/chat/{kwargs["pk"]}/messages/')


class BannerTimeTable(APIView):
    def get(self, request, *args, **kwargs):
        return Request2Mail(request, f'{MAIL_HOST}/timetable/{kwargs["pk"]}/')


class BannerTimeTables(APIView):
    def get(self, request, *args, **kwargs):
        return Request2Mail(request, f'{MAIL_HOST}/timetables/')


class Banner(APIView):
    def post(self, request, *args, **kwargs):
        return RequestWithFile2Mail(request, f'{MAIL_HOST}/banner/', 'image')

    def get(self, request, *args, **kwargs):
        return Request2Mail(request, f'{MAIL_HOST}/banner/{kwargs["pk"]}/')

    def delete(self, request, *args, **kwargs):
        return Request2Mail(request, f'{MAIL_HOST}/banner/{kwargs["pk"]}/')

    def put(self, request, *args, **kwargs):
        return RequestWithFile2Mail(request, f'{MAIL_HOST}/banner/{kwargs["pk"]}/', 'image')


class GetAllBanners(APIView):
    def get(self, request, *args, **kwargs):
        link = f'{MAIL_HOST}/banners/?'
        if request.GET.get('wallet'):
            link += f'wallet={request.GET.get("wallet")}'
        if request.GET.get('timeTable'):
            link += f'timeTable={request.GET.get("timeTable")}'
        if request.GET.get('title'):
            link += f'title={request.GET.get("title")}'
        if request.GET.get('link'):
            link += f'link={request.GET.get("link")}'
        if request.GET.get('status'):
            link += f'status={request.GET.get("status")}'
        return Request2Mail(request, link)
