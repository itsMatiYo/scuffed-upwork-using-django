from authentication.utils import (
    send_request_to_server,
)
from rest_framework import exceptions
from wallet.serializer import (
    Spend_Type_Two_Serializer,
)
from decouple import config

# * Server Information :
HOST_WALLET = config('HOST_WALLET')
CREDITCARD_URL = HOST_WALLET + "/creditcard/"
GIFTCARD_URL = HOST_WALLET + "/creditcard/giftcard/"
TOKEN = config('TOKEN')
BASE_AUTH = config('BASE_AUTH')
SERVICE_ID = config('SERVICE_ID')


def spend_from_card_data(amount, wallet_id, cart_id, sections_wallet_id, sections_percent):
    data_spend_from_card = {
        "amount": amount,
        "wallet_id": wallet_id,
        "service_id": SERVICE_ID,
        "description": "buy class with Card",
        "cart_id": cart_id,
        "sections": [
            {
                "wallet_id": sections_wallet_id,
                "percent": sections_percent
            }
        ]
    }
    return data_spend_from_card


# todo : Spend from  card |card_type --> [creditcard,giftcard] data --> {cart_id,amount,password,service_id,wallet_id,section=[],expire_at, description}
def spend_from_card(card_type, data):

    serializer = Spend_Type_Two_Serializer(data=data)

    if serializer.is_valid():

        if card_type == "creditcard":
            url = CREDITCARD_URL + data["cart_id"] + "/spend"
        elif card_type == "giftcard":
            url = GIFTCARD_URL + data["cart_id"] + "/spend"
        else:
            raise exceptions.ValidationError(detail="Invalid type", code=400)

        response = send_request_to_server(
            url=url, serializer=serializer, request_type="post", token=TOKEN, data_type="json")

        if response.data['status'] == True:
            return response.data
        else:
            raise exceptions.ValidationError(
                detail=response.data, code=response.status_code)
    else:
        raise exceptions.ValidationError(detail="Invalid data", code=400)
