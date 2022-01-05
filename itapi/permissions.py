from rest_framework.permissions import BasePermission


class CreateRead(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['POST', 'GET']
