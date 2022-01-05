from django.db.models.aggregates import Count
from django.http.response import Http404
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
import json
from decouple import config
import jwt
from itapi.models import City
from users.models import CityAdmin, Customer, Employee, Visitor, Wallet
from django.core.exceptions import ObjectDoesNotExist

# ! Server Information :
HOST = config('HOST')
AUTH_SECRET_KEY = config('AUTH_SECRET_KEY')
BASE_AUTH = config('BASE_AUTH')
SERVICE_ID = config('SERVICE_ID')
ROLE_ID_EMPLOYEE = config('ROLE_ID_EMPLOYEE')
ROLE_ID_CUSTOMER = config('ROLE_ID_CUSTOMER')
ROLE_ID_CITYADMIN = config('ROLE_ID_CITYADMIN')
ROLE_ID_VISITOR = config('ROLE_ID_VISITOR')


# todo : Get Wallet
def get_wallet(token):
    try:
        decoded = jwt.decode(token.split(
            " ")[-1], AUTH_SECRET_KEY, algorithms=["HS256"])
        wallet_id = decoded['wallet_id']
        wallet_object = Wallet.objects.get(id=wallet_id)
    except ObjectDoesNotExist:
        raise exceptions.ValidationError(
            detail="ٌWallet object not exist", code=400)
    except:
        raise exceptions.ValidationError(
            detail="ٌcan\'n return wallet object", code=400)
    return wallet_object


# todo : verify token
def verify_token(token):
    try:
        jwt.decode(
            token, AUTH_SECRET_KEY, algorithms=["HS256"])
    except:
        return False

    return True


# todo : verify token for admin
def verify_token_for_admin(token):
    try:
        data = jwt.decode(
            token, AUTH_SECRET_KEY, algorithms=["HS256"])
    except:
        return False

    if data['role'] == "admin":
        return True
    else:
        return False


# todo : Sent request and return response to client | requests data can set in data or serializer
def send_request_to_server(url, request_type, serializer=None, token=None, data_type=None, data={}):
    if request_type == "post":

        # * for post method without serializer
        if not serializer == None:
            data = dict(serializer.validated_data)

        # * Set auth_basic for acceptable request & token ( can be None )
        headers = {
            'auth_basic': BASE_AUTH,
            'Authorization': token,
        }

        # ! for request with nested datetime's object can't use data and should use json
        if data_type == "json":
            response = requests.post(url, json=data, headers=headers)
        elif data_type == "files":
            response = requests.post(url, files=data, headers=headers)
        else:
            response = requests.post(url, data=data, headers=headers)

        return Response(response.json(), status=response.status_code)

    elif request_type == "delete":

        # * for post method without serializer
        if not serializer == None:
            data = dict(serializer.validated_data)

        # * Set auth_basic for acceptable request & token ( can be None )
        headers = {
            'auth_basic': BASE_AUTH,
            'Authorization': token,
        }
        response = requests.delete(url, json=data, headers=headers)

        return Response(response.json(), status=response.status_code)

    elif request_type == "get":

        # * Set auth_basic for acceptable request & token ( can be None )
        headers = {
            'auth_basic': BASE_AUTH,
            'Authorization': token,
        }
        response = requests.get(url, headers=headers)

        return Response(response.json(), status=response.status_code)


# todo : Grt token
def get_token(request):
    if 'Authorization' in request.headers:
        return request.headers['Authorization'].split(" ")[-1]
    else:
        raise exceptions.ValidationError(
            detail="ٌCan\'t found Token", code=404)


# todo : Create url ( with ROLE_ID )
def get_url_with_service_and_role(user_type, main_url):
    # * Check type for roles :
    if user_type == "employee":
        url = HOST + main_url + ROLE_ID_EMPLOYEE + "/" + SERVICE_ID
    elif user_type == "visitor":
        url = HOST + main_url + ROLE_ID_VISITOR + "/" + SERVICE_ID
    elif user_type == "customer":
        url = HOST + main_url + ROLE_ID_CUSTOMER + "/" + SERVICE_ID
    elif user_type == "cityadmin":
        url = HOST + main_url + ROLE_ID_CITYADMIN + "/" + SERVICE_ID
    elif user_type == "admin":
        url = HOST + "/admin" + main_url
    else:
        raise exceptions.ValidationError(detail="Invalid type", code=400)

    return url


# todo DRY : Create url for login ( admin or user )
def get_url_admin_or_user(user_type, main_url):
    # * Check type for roles :
    if user_type == "admin":
        url = HOST + "/admin" + main_url
    elif user_type == "user":
        url = HOST + main_url
    else:
        raise exceptions.ValidationError(detail="Invalid type", code=400)

    return url


def get_my_expert(request):
    token = get_token(request)
    wallet = get_wallet(token)
    try:
        obj = Employee.objects.get(wallet=wallet)
        obj = obj.expert
        return obj
    except:
        raise Http404


def get_my_object(request, model):
    token = get_token(request)
    wallet = get_wallet(token)
    try:
        obj = model.objects.get(wallet=wallet)
        return obj
    except:
        raise Http404


def is_it_admin(request):
    try:
        token = get_token(request)
        return verify_token_for_admin(token)
    except:
        return False


def is_it_its(request, model):
    try:
        token = get_token(request)
        wallet = get_wallet(token)
    except:
        return False
    try:
        obj = model.objects.filter(wallet=wallet)
    except:
        return False
    if obj.exists():
        return True
    return False


def is_it_expert(request):
    try:
        token = get_token(request)
    except:
        return False
    try:
        wallet = get_wallet(token)
        obj = Employee.objects.get(wallet=wallet)
        if obj.expert:
            return True
        else:
            return False
    except:
        return False


def get_my_expert(request):
    try:
        token = get_token(request)
        wallet = get_wallet(token)
    except:
        return False
    try:
        obj = Employee.objects.get(wallet=wallet)
        obj = obj.expert
        return obj
    except:
        raise Http404


def check_city(obj_type, city):
    if obj_type == "employee":
        try:
            city.city_admin
            return city
        except:
            return City.objects.annotate(emp_count=Count('employee')).order_by('emp_count')[0]
    elif obj_type == "visitor":
        try:
            city.city_admin
            return city
        except:
            raise exceptions.ValidationError(
                {'city': 'This city does not have cityadmin'})
    else:
        return city


def create_obj_by_type(obj_type, new_wallet, city):
    if obj_type == "employee":
        Employee.objects.create(wallet=new_wallet, city=city)

    elif obj_type == "visitor":
        Visitor.objects.create(wallet=new_wallet, city=city)
    elif obj_type == "customer":
        Customer.objects.create(wallet=new_wallet, city=city)
    elif obj_type == "cityadmin":
        CityAdmin.objects.create(wallet=new_wallet, city=city)
    else:
        raise exceptions.ValidationError(detail="Invalid data", code=400)


def get_wallet_without_verify(request):
    token = get_token(request)
    wallet = get_wallet(token)
    return wallet


# todo : Create url ( for Address )
def get_url_for_address(user_type, main_url):
    if user_type == 'user':
        url = HOST + main_url
    elif user_type == "admin":
        url = HOST + "/admin" + main_url + "/my"
    else:
        raise exceptions.ValidationError(
            detail="Invalid user type", code=400)
    return url
