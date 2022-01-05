from rest_framework.views import APIView
from authentication.utils import (
    get_token,
    send_request_to_server,
)
from rest_framework import exceptions
from wallet.serializer import (
    Filter_Transaction_Serializer,
    PaymentSerializer,
)
from authentication.permission import (
    AdminPermission,
)
from decouple import config

# * Server Information :
HOST_WALLET = config('HOST_WALLET')
TRANSACTION_URL = HOST_WALLET + "/transaction/"


# * Transaction : All objects
class Transaction_All(APIView):
    permission_classes = [AdminPermission]
    serializer_class = Filter_Transaction_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            token = get_token(request)
            url = TRANSACTION_URL
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Transaction : Retrieve object
class Transaction_Get_One(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        token = get_token(request)
        url = TRANSACTION_URL + kwargs["id"]
        return send_request_to_server(url, "get", token=token)


# * Transaction : All objects in Action --> [need-action , holds , accepted , rejected , unpaied-taxes]
class Transaction_Action_Get_All(APIView):
    permission_classes = [AdminPermission]
    serializer_class = Filter_Transaction_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = TRANSACTION_URL + kwargs["action"]
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token, data_type="json")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Transaction : Set Hold
class Transaction_Hold(APIView):
    permission_classes = [AdminPermission]

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        url = TRANSACTION_URL + kwargs["id"] + "/hold"
        return send_request_to_server(url=url, request_type="post", token=token)


# * Transaction: Set Accept
class Transaction_Accept(APIView):
    permission_classes = [AdminPermission]

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        url = TRANSACTION_URL + kwargs["id"] + "/accept"
        data = {
            "commission_status": {
                "{{$guid}}": kwargs["commission"]
            }
        }
        return send_request_to_server(url=url, data=data, request_type="post", token=token)


# * Transaction : Set Reject
class Transaction_Reject(APIView):
    permission_classes = [AdminPermission]

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        url = TRANSACTION_URL + kwargs["id"] + "/reject"
        return send_request_to_server(url=url, request_type="post", token=token)


# * Transaction : Set Tax
class Transaction_Tax(APIView):
    permission_classes = [AdminPermission]
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = TRANSACTION_URL + kwargs["id"] + "/tax"
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)
