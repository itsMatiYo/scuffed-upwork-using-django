import requests
from rest_framework import status
from rest_framework.response import Response

from authentication.utils import get_token
from rest_framework.exceptions import ValidationError


def validate_file(file):
    file_size = file.file.size
    limit_mb = 10
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("The file must be less than 10MB")


def Request2Mail(request, link):
    headers = {'Authorization': get_token(request)}

    if request.method == 'POST':
        req = requests.post(link, headers=headers, data=dict(request.data))
        return Response(data=req.json(), status=req.status_code)
    elif request.method == 'GET':
        req = requests.get(link, headers=headers)
        return Response(data=req.json(), status=req.status_code)
    elif request.method == 'PUT':
        req = requests.put(link, headers=headers, data=dict(request.data))
        return Response(data=req.json(), status=req.status_code)
    elif request.method == 'DELETE':
        req = requests.delete(link, headers=headers)
        if req.status_code == 204:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(req.json())


def RequestWithFile2Mail(request, link, fileName):
    headers = {'Authorization': get_token(request)}
    if request.data:
        data = dict(request.data)
    else:
        raise ValidationError('There is no data')

    if request.method == 'POST':
        if fileName in request.data:
            file = request.data[fileName]
            req = requests.post(link, data=data, files={fileName: file},
                                headers=headers)
            return Response(data=req.json(), status=req.status_code)
        req = requests.post(link, headers=headers, data=dict(request.data))
        return Response(data=req.json(), status=req.status_code)

    elif request.method == 'PUT':
        if fileName in request.data:
            file = request.data[fileName]
            req = requests.put(link, data=data, files={fileName: file},
                               headers=headers)
            return Response(data=req.json(), status=req.status_code)
        req = requests.put(link, data=data, headers=headers)
        return Response(data=req.json(), status=req.status_code)


def SendCustomPostRequest2Mail(request, data, link):
    headers = {'Authorization': get_token(request)}
    req = requests.post(link, headers=headers, data=data)
    print(req.json())
    return Response(data=req.json(), status=req.status_code)
