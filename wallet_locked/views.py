from rest_framework.views import APIView
from authentication.utils import (
    get_token,
    send_request_to_server,
)
from rest_framework import exceptions
from wallet.serializer import (
    FilterSerializer,
    PaymentSerializer,
    Description_Serializer,
    Spend_Type_one_Serializer,
)
from authentication.permission import (
    AdminOrUserReadOnly,
    AdminPermission,
)
from decouple import config

# * Server Information :
HOST_WALLET = config('HOST_WALLET')
LOCKED_URL = HOST_WALLET + "/locked/"


# * locked : All objects
class Locked_All(APIView):
    permission_classes = [AdminOrUserReadOnly]
    serializer_class = FilterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = LOCKED_URL
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token, data_type="json")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * locked : Create object
class Locked_Create(APIView):
    permission_classes = [AdminPermission]
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = LOCKED_URL + "new"
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * locked : Update - Retrieve object
class Locked_UR(APIView):
    permission_classes = [AdminOrUserReadOnly]
    serializer_class = Description_Serializer

    def get(self, request, *args, **kwargs):
        token = get_token(request)
        url = LOCKED_URL + kwargs["id"]
        return send_request_to_server(url, "get", token=token)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = LOCKED_URL + kwargs["id"]
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * locked : Unlocked object
class Locked_Unlocked(APIView):
    permission_classes = [AdminPermission]
    serializer_class = Spend_Type_one_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = LOCKED_URL + kwargs["id"] + "/unlocked"
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token, data_type="json")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * locked : Deduct Money
class Locked_Deduct_Money(APIView):
    permission_classes = [AdminPermission]
    serializer_class = Spend_Type_one_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = LOCKED_URL + kwargs["id"] + "/deduct-money"
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token, data_type="json")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)
