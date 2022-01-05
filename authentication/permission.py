from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from users import models
from authentication.utils import (
    get_token,
    get_wallet,
    is_it_expert,
    verify_token,
    verify_token_for_admin,
)


class EmployeePermissionUnapproved(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = get_token(request)
        except:
            return False
        if verify_token(token):
            try:
                wallet = get_wallet(token)
            except:
                return False
            return models.Employee.objects.filter(wallet=wallet).exists()
        else:
            return False


class EmployeePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = get_token(request)
        except:
            return False
        if verify_token(token):
            try:
                wallet = get_wallet(token)
            except:
                return False
            emp = get_object_or_404(models.Employee, wallet=wallet)
            return emp.approved
        else:
            return False


class ExpertPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_it_expert(request)


class VisitorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = get_token(request)
        except:
            return False
        if verify_token(token):
            try:
                wallet = get_wallet(token)
            except:
                return False
            vs = get_object_or_404(models.Visitor, wallet=wallet)
            return vs.approved
        else:
            return False


class VisitorPermissionUnapproved(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token = get_token(request)
        except:
            return False
        if verify_token(token):
            try:
                wallet = get_wallet(token)
            except:
                return False
            return models.Visitor.objects.filter(wallet=wallet).exists()
        else:
            return False


class CustomerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = get_token(request)
        except:
            return False
        if verify_token(token):
            try:
                wallet = get_wallet(token)
            except:
                return False
            return models.Customer.objects.filter(wallet=wallet).exists()
        else:
            return False


class CityAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = get_token(request)
            if verify_token(token):
                try:
                    wallet = get_wallet(token)
                except:
                    return False
                return models.CityAdmin.objects.filter(wallet=wallet).exists()
            else:
                return False
        except:
            return False


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = get_token(request)
        except:
            return False
        return verify_token_for_admin(token)


class AdminOrUserReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = get_token(request)
        except:
            return False
        if request.method in SAFE_METHODS:
            return True
        else:
            return verify_token_for_admin(token)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class Admin_And_User(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = get_token(request)
        except:
            return False
        if verify_token_for_admin(token) or verify_token(token):
            return True
        return False
