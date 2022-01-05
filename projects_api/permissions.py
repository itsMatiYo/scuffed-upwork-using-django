from rest_framework.permissions import BasePermission

from authentication.utils import get_my_expert, get_my_object
from users.models import CityAdmin, Customer, Employee, Expert, Visitor


class EmployeeInProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        employee = get_my_object(request, Employee)
        if employee in obj.employees.all():
            return True
        return False


class ProjectCustomerOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        customer = get_my_object(request, Customer)
        if customer == obj.customer:
            return True
        return False


class VisitorInProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        visitor = get_my_object(request, Visitor)
        if visitor == obj.visitor:
            return True
        return False


class ExpertInProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        expert = get_my_expert(request, Expert)
        return expert.verifies.filter(project=obj).exists()


class CityAdminInProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        cityadmin = get_my_object(request, CityAdmin)
        return cityadmin.city == obj.city


class ExpertTopPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            expert = get_my_expert(request)
            return expert.is_it_top()
        except:
            return False


class ExpertTopInProject(BasePermission):
    def has_object_permission(self, request, view, obj):
        expert = get_my_expert(request)
        if expert.is_it_top():
            return expert.verifies.filter(project=obj).exists()
        return False


class ExpertIsOwnerEmp(BasePermission):
    def has_object_permission(self, request, view, obj):
        expert = get_my_expert(request)
        return obj.ve.expert == expert
