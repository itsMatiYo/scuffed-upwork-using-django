from rest_framework.views import APIView
from authentication.utils import (
    get_token,
    send_request_to_server,
)
from rest_framework import exceptions
from wallet.serializer import (
    FilterSerializer,
    PaymentSerializer,
)
from authentication.permission import AdminOrUserReadOnly
from decouple import config

# * Server Information :
HOST_WALLET = config('HOST_WALLET')
PAYMENT_URL = HOST_WALLET + "/payment/"


# * Payment : All objects
class Payment_All(APIView):
    permission_classes = [AdminOrUserReadOnly]
    serializer_class = FilterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = PAYMENT_URL
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token, data_type="json")
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)


# * Payment : Retrieve objects
class Payment_R(APIView):
    permission_classes = [AdminOrUserReadOnly]

    def get(self, request, *args, **kwargs):
        token = get_token(request)
        url = PAYMENT_URL + kwargs["id"]
        return send_request_to_server(url=url, request_type="get", token=token)


# * Payment : Create objects
#  ! [99/6/5] --> wallet server not work yet !
class Payment_Create(APIView):
    permission_classes = [AdminOrUserReadOnly]
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token = get_token(request)
            url = PAYMENT_URL + "new"
            return send_request_to_server(url=url, serializer=serializer, request_type="post", token=token)
        else:
            raise exceptions.ValidationError(detail="Invalid data", code=400)
