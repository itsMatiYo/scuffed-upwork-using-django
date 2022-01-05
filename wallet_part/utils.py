from authentication.utils import (
    send_request_to_server,
)
from rest_framework import exceptions
from wallet.serializer import (
    Part_Create_Serializer,
    Spend_Type_one_Serializer,
)
from decouple import config

# * Server Information :
HOST_WALLET = config('HOST_WALLET')
BASE_AUTH = config('BASE_AUTH')
TOKEN = config('TOKEN')
SERVICE_ID = config('SERVICE_ID')
PART_URL = HOST_WALLET + "/part/"


def create_part_data(wallet_id, amount):
    data_create_part = {
        "service_id": SERVICE_ID,
        "wallet_id": wallet_id,
        "name": "create part",
        "amount": amount,
    }
    return data_create_part


# todo : Create Part with data --> {service_id,wallet_id,name,amount} and return part id
def create_part(data):
    serializer = Part_Create_Serializer(data=data)

    if serializer.is_valid():
        url = PART_URL + "new"
        create_part_response = send_request_to_server(
            url=url, serializer=serializer, request_type="post", token=TOKEN)
        if create_part_response.data["status"] == True:
            part_id = create_part_response.data["data"]["part"]["id"]
            return part_id
        else:
            raise exceptions.ValidationError(
                detail=create_part_response.data, code=create_part_response.status_code)
    else:
        raise exceptions.ValidationError(detail="Invalid data", code=400)


def spend_part_data(amount, sections):
    data_spend_from_part = {
        "amount": amount,
        "service_id": SERVICE_ID,
        "description": "buy adviser from wallet",
        "sections": sections,
    }
    return data_spend_from_part


# todo : Spend from  part and return response to client | data --> {amount, service_id, description, section=[]} and return response's data
def spend_from_part(part_id, data):
    serializer = Spend_Type_one_Serializer(data=data)

    if serializer.is_valid():
        url = PART_URL + "/" + part_id + "/spend"
        response = send_request_to_server(
            url=url, serializer=serializer, request_type="post", token=TOKEN, data_type="json")
        if response.data['status'] == True:
            return response.data
        else:
            raise exceptions.ValidationError(
                detail=response.data, code=response.status_code)
    else:
        raise exceptions.ValidationError(detail="Invalid data", code=400)
