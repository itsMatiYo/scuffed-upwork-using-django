from rest_framework.views import APIView
from authentication.utils import (
    get_token,
    send_request_to_server,
)
from rest_framework import exceptions
from wallet.serializer import (
    FilterSerializer,
    Withdrawal_Create_Serializer,
    Withdrawal_UJ_Serializer,
)
from authentication.permission import (
    AdminOrUserReadOnly,
    AdminPermission,
)
from decouple import config

# * Server Information :
HOST_WALLET = config('HOST_WALLET')
WITHDRAWAL_URL = HOST_WALLET + "/Withdrawal/"


# * Withdrawal : All objects
class Withdrawal_All(APIView):
    permission_classes = [AdminOrUserReadOnly]
    serializer_class = FilterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = WITHDRAWAL_URL
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token, data_type="json")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Withdrawal : Create objects
class Withdrawal_Create(APIView):
    permission_classes = [AdminOrUserReadOnly]
    serializer_class = Withdrawal_Create_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = WITHDRAWAL_URL + "new"
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Withdrawal : Update - Retrieve object
class Withdrawal_UR(APIView):
    permission_classes = [AdminOrUserReadOnly]
    serializer_class = Withdrawal_UJ_Serializer

    def get(self, request, *args, **kwargs):
        token = get_token(request)
        url = WITHDRAWAL_URL + kwargs["id"]
        return send_request_to_server(url, "get", token=token)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = WITHDRAWAL_URL + kwargs["id"]
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Withdrawal : Accept object
class Withdrawal_Accept(APIView):
    permission_classes = [AdminPermission]
    serializer_class = Withdrawal_UJ_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = WITHDRAWAL_URL + kwargs["id"] + "/accept"
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Withdrawal : Reject object
class Withdrawal_Reject(APIView):
    permission_classes = [AdminPermission]
    serializer_class = Withdrawal_UJ_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = WITHDRAWAL_URL + kwargs["id"] + "/reject"
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)
