from rest_framework.views import APIView
from authentication.views import (
    get_token,
    send_request_to_server,
)
from rest_framework import exceptions
from wallet.serializer import (
    FilterSerializer,
    Card_Serializer,
    Gitcard_Serializer,
)
from authentication.permission import (
    AdminPermission,
)
from decouple import config

# * Server Information :
HOST_WALLET = config('HOST_WALLET')
CREDITCARD_URL = HOST_WALLET + "/creditcard/"
GIFTCARD_URL = HOST_WALLET + "/creditcard/giftcard/"


# * CREADITCARD : Create Creditcard
class Creditcard_Create(APIView):
    permission_classes = [AdminPermission]
    serializer_class = Card_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = CREDITCARD_URL + "new"
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * GIFITCARD : Create Giftcard
class Giftcard_Create(APIView):
    permission_classes = [AdminPermission]
    serializer_class = Gitcard_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = GIFTCARD_URL + "new"
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * CARD : All Card objects
class Card_All(APIView):
    permission_classes = [AdminPermission]
    serializer_class = FilterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = CREDITCARD_URL
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token, data_type="json")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * CARD : Retrieve Card
class Card_One(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, *args, **kwargs):
        token = get_token(request)
        url = CREDITCARD_URL + kwargs["id"]
        return send_request_to_server(url, "get", token=token)
