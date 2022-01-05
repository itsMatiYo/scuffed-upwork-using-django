from authentication.serializer import *
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.models import Wallet
from rest_framework import exceptions
from authentication.permission import AdminPermission, Admin_And_User
from authentication.utils import BASE_AUTH, HOST, check_city, create_obj_by_type, get_token, get_url_admin_or_user, get_url_for_address, get_url_with_service_and_role, is_it_admin, send_request_to_server


# * Auth : Get One User object
class GetUser(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        token = get_token(request)
        url = HOST + "/admin/users/" + kwargs["id"]
        return send_request_to_server(url, "get", token=token)


# * Auth : All Users
class AllUser(APIView):
    permission_classes = [AdminPermission]
    serializer_class = FilterSerializer

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        url = HOST + "/admin/users"
        return send_request_to_server(url=url, request_type="post", token=token)


# * Auth : Register User
class Register(APIView):
    serializer_class = RegisterSrializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # ! cant register admin
            if kwargs["type"] == "admin":
                raise exceptions.ValidationError(
                    detail="Cant register admin", code=400)
            if kwargs["type"] == "cityadmin":
                if not is_it_admin(request):
                    raise exceptions.ValidationError(
                        detail="just admin can register city admin", code=400)
            city = check_city(
                kwargs["type"], serializer.validated_data.get('city'))
            url = get_url_with_service_and_role(kwargs["type"], "/register/")
            response = requests.post(
                url, dict(serializer.validated_data), headers={'auth_basic': BASE_AUTH})
            js_response = response.json()
            if js_response['status'] != False:
                wallet_id = js_response['data']['wallet']['id']
                # ? Create wallet object
                new_wallet = Wallet.objects.create(id=wallet_id)
                # ? Create user object
                create_obj_by_type(
                    kwargs["type"], new_wallet, city)
                return Response(js_response, status=response.status_code)
            else:
                raise exceptions.ValidationError(
                    detail=js_response, code=response.status_code)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# * Auth : Login User
class Login(APIView):
    serializer_class = LoginSrializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = get_url_with_service_and_role(kwargs["type"], "/login/")
            return send_request_to_server(url=url, serializer=serializer, request_type="post")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Auth : User Info
class MyUserInfo(APIView):

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        url = get_url_admin_or_user(kwargs["type"], "/me")
        return send_request_to_server(url=url, request_type="post", token=token)


# * Auth : Update User Info
class MyInfoUpdate(APIView):
    serializer_class = UpdateSrializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = get_url_admin_or_user(kwargs["type"], "/me/update")
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Auth : Logout User
class Logout(APIView):

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        url = get_url_admin_or_user(kwargs["type"], "/logout")
        return send_request_to_server(url=url, request_type="post", token=token)


# * Auth : Delete User
class DeleteAccount(APIView):
    serializer_class = DeleteSrializer

    def delete(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = HOST + "/delete-my-account"
            token = get_token(request)
            return send_request_to_server(url=url, serializer=serializer, request_type="delete", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Auth : Update Token
class UpdateToken(APIView):
    serializer_class = RefreshTokenSrializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = HOST + "/update-token"
            return send_request_to_server(url=url, serializer=serializer, request_type="post")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Address : Update + Get + Create
class MyAddress(APIView):
    permission_classes = [Admin_And_User]
    serializer_class = AddressSrializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user_type = kwargs['user_type']
        if serializer.is_valid():
            token = get_token(request)
            url = get_url_for_address(user_type, main_url="/address")
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)

    def get(self, request, *args, **kwargs):
        user_type = kwargs['user_type']
        token = get_token(request)
        url = get_url_for_address(user_type, main_url="/address")
        return send_request_to_server(url=url, request_type="get", token=token)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user_type = kwargs['user_type']
        if serializer.is_valid():
            token = get_token(request)
            addressId = request.data.get('id', None)
            if user_type == 'user':
                url = HOST + "/address/" + str(addressId)
            elif user_type == "admin":
                url = HOST + "/admin/address/" + str(addressId)
            else:
                raise exceptions.ValidationError(
                    detail="Invalid user type", code=400)
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)


# * Address : Get all + one
class AddressSee(APIView):
    permission_classes = [AdminPermission]
    serializer_class = FilterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = HOST + "/admin/address/"
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)

    def get(self, request, *args, **kwargs):
        addressId = request.data.get('id', None)
        token = get_token(request)
        url = HOST + "/admin/address/" + str(addressId)
        return send_request_to_server(url=url, request_type="get", token=token)


# * Company : Update + Get + Create
class MyCompany(APIView):
    permission_classes = [Admin_And_User]
    serializer_class = CompanySrializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user_type = kwargs['user_type']
        if serializer.is_valid():
            token = get_token(request)
            url = get_url_for_address(user_type, main_url="/company")
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)

    def get(self, request, *args, **kwargs):
        user_type = kwargs['user_type']
        token = get_token(request)
        url = get_url_for_address(user_type, main_url="/company")
        return send_request_to_server(url=url, request_type="get", token=token)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user_type = kwargs['user_type']
        if serializer.is_valid():
            token = get_token(request)
            companyid = request.data.get('id', None)
            if user_type == 'user':
                url = HOST + "/company/" + str(companyid)
            elif user_type == "admin":
                url = HOST + "/admin/company/" + str(companyid)
            else:
                raise exceptions.ValidationError(
                    detail="Invalid user type", code=400)
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)


# * Company : Get all + one
class CompanySee(APIView):
    permission_classes = [AdminPermission]
    serializer_class = FilterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = HOST + "/admin/company/"
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)

    def get(self, request, *args, **kwargs):
        companyid = request.data.get('id', None)
        token = get_token(request)
        url = HOST + "/admin/company/" + str(companyid)
        return send_request_to_server(url=url, request_type="get", token=token)


# * Social Media : Get + Create
class MySocialMedia(APIView):
    permission_classes = [Admin_And_User]
    serializer_class = SocialMediaSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user_type = kwargs['user_type']
        if serializer.is_valid():
            token = get_token(request)
            url = get_url_for_address(user_type,  main_url="/social-media")
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)

    def get(self, request, *args, **kwargs):
        user_type = kwargs['user_type']
        token = get_token(request)
        url = get_url_for_address(user_type, main_url="/social-media")
        return send_request_to_server(url=url, request_type="get", token=token)


# * Social Media : Get all + one + Update
class SocialMediaSee(APIView):
    permission_classes = [AdminPermission]
    serializer_class = FilterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = HOST + "/admin/social-media/"
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)

    def get(self, request, *args, **kwargs):
        mediaid = request.data.get('id', None)
        token = get_token(request)
        url = HOST + "/admin/social-media/" + str(mediaid)
        return send_request_to_server(url=url, request_type="get", token=token)

    def patch(self, request, *args, **kwargs):
        serializer = SocialMediaSerializer(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            mediaid = request.data.get('id', None)
            url = HOST + "/admin/social-media/" + str(mediaid)
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)


# * Info : Update + Get + Create
class MyInfo(APIView):
    permission_classes = [Admin_And_User]
    serializer_class = InfoSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user_type = kwargs['user_type']
        if serializer.is_valid():
            token = get_token(request)
            url = get_url_for_address(user_type, main_url="/info")
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)

    def get(self, request, *args, **kwargs):
        user_type = kwargs['user_type']
        token = get_token(request)
        url = get_url_for_address(user_type, main_url="/info")
        return send_request_to_server(url=url, request_type="get", token=token)


# * Info : Get all + one
class InfoSee(APIView):
    permission_classes = [AdminPermission]
    serializer_class = FilterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = HOST + "/admin/info/"
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)

    def get(self, request, *args, **kwargs):
        infoid = request.data.get('id', None)
        token = get_token(request)
        url = HOST + "/admin/info/" + str(infoid)
        return send_request_to_server(url=url, request_type="get", token=token)

    def patch(self, request, *args, **kwargs):
        serializer = InfoSerializer(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            infoid = request.data.get('id', None)
            url = HOST + "/admin/info/" + str(infoid)
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)


# * Session :
class Session(APIView):
    permission_classes = [AdminPermission]

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        sessionId = request.data.get('sessionId', None)
        url = HOST + "/admin/session/"+sessionId
        return send_request_to_server(url=url, request_type="post", data=request.data, token=token)


# * Session :
class SessionSee(APIView):
    permission_classes = [Admin_And_User]

    def post(self, request, *args, **kwargs):
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            user_type = kwargs['user_type']
            token = get_token(request)
            url = get_url_admin_or_user(user_type, "/session")
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)

    def delete(self, request, *args, **kwargs):
        token = get_token(request)
        url = get_url_admin_or_user(
            user_type=kwargs['user_type'], main_url="/session/" + str(request.data.get('id', None)))
        return send_request_to_server(url=url, request_type="delete", token=token)


class AdminSecurity(APIView):
    # permission_classes = [AdminPermission]

    def post(self, request, *args, **kwargs):
        serializer = AdminSecuritySerializer(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = HOST + "/super-admin/security-question"
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)

    def get(self, request, *args, **kwargs):
        serializer = FilterSerializer(data=request.data)
        if serializer.is_valid():
            infoid = request.data.get('id', None)
            token = get_token(request)
            url = HOST + "/super-admin/security-question"
            return send_request_to_server(url=url, request_type="get", token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)

    def patch(self, request, *args, **kwargs):
        serializer = AdminSecuritySerializer(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            securityid = request.data.get('id', None)
            url = HOST + "/super-admin/security-question/" + str(securityid)
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)


class SecurityQuestions(APIView):
    permission_classes = [Admin_And_User]

    def get(self, request, *args, **kwargs):
        token = get_token(request)
        url = HOST + "/security-questions"
        return send_request_to_server(url=url, request_type="get", token=token)


class SecurityAnswer(APIView):
    permission_classes = [Admin_And_User]

    def post(self, request, *args, **kwargs):
        serializer = AnsewerSecuritySerializer(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = HOST + "/security-answer"
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)


class RecoveryByLastPassword(APIView):
    permission_classes = [Admin_And_User]

    def post(self, request, *args, **kwargs):
        serializer = Recovery1Serializer(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = HOST + "/recovery/by-last-password"
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)


class RecoveryNewPassword(APIView):
    permission_classes = [Admin_And_User]

    def post(self, request, *args, **kwargs):
        serializer = Recovery2Serializer(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = HOST + "/recovery/new-password"
            return send_request_to_server(url=url, request_type="post", serializer=serializer, token=token)
        else:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)
