from rest_framework.views import APIView
from wallet.serializer import (
    EditOptionSerializer,
    FilterSerializer,
)
from authentication.utils import (
    get_token,
    send_request_to_server,
)
from authentication.permission import AdminPermission
from rest_framework import exceptions
from decouple import config

# * Server Information :
HOST_WALLET = config('HOST_WALLET')
PACKET_URL = HOST_WALLET + "/packet/"


# * Packet : All objs
class Packet_All(APIView):
    permission_classes = [AdminPermission]
    serializer_class = FilterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = PACKET_URL
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Packet : Update and Retrieve packet obj
class Packet_UR(APIView):
    permission_classes = [AdminPermission]
    serializer_class = EditOptionSerializer

    def get(self, request, *args, **kwargs):
        token = get_token(request)
        url = PACKET_URL + kwargs["id"]
        return send_request_to_server(url, "get", token=token)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = PACKET_URL + kwargs["id"]
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)
