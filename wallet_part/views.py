from rest_framework.views import APIView
from authentication.utils import (
    get_token,
    send_request_to_server,
)
from rest_framework import exceptions
from wallet.serializer import (
    FilterSerializer,
    NameSerializer,
)
from authentication.permission import (
    AdminPermission,
)
from rest_framework.response import Response
from decouple import config

# * Server Information :
HOST_WALLET = config('HOST_WALLET')
PART_URL = HOST_WALLET + "/part/"


# * Part : All objects
class Part_All(APIView):
    permission_classes = [AdminPermission]
    serializer_class = FilterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = PART_URL
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token, data_type="json")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Part : Update - Delete - Retrieve objects
class Part_UDR(APIView):
    permission_classes = [AdminPermission]
    serializer_class = NameSerializer

    def get(self, request, *args, **kwargs):
        token = get_token(request)
        url = PART_URL + kwargs["id"]
        return send_request_to_server(url, "get", token=token)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = PART_URL + kwargs["id"]
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)

    def delete(self, request, *args, **kwargs):
        token = get_token(request)
        url = PART_URL + kwargs["id"]
        return send_request_to_server(url, "delete", token=token)
