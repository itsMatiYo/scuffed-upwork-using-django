from django.utils import timezone
from django.http import Http404
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from itapi.serializers import ReportEmployeeSerializer4admin
from projects_api.models import Project, VerifyExpert
from users.models import CityAdmin, Customer, Expert
from itapi.models import TimeTableVisitor
from users.models import Visitor
from authentication.utils import is_it_admin, is_it_expert, is_it_its, get_my_object, get_my_expert
from authentication.permission import AdminPermission, CityAdminPermission, CustomerPermission, ExpertPermission, ReadOnly, VisitorPermission
from rest_framework import request, viewsets, generics
from users.models import CityAdmin, Employee
from itapi import models, serializers
from authentication.utils import get_my_object, is_it_admin, is_it_its
from authentication.permission import AdminPermission, ReadOnly
from rest_framework import generics, viewsets
from django.shortcuts import get_object_or_404
from .permissions import CreateRead


class CategoryList(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer4Admin
    permission_classes = [AdminPermission | ReadOnly]

    def get_serializer_class(self):
        req = self.request
        if is_it_admin(req):
            return serializers.CategorySerializer4Admin
        else:
            return serializers.CategorySerializerReadOnly


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    # add admin city for adding people
    permission_classes = [AdminPermission | ReadOnly]
    queryset = models.Category.objects.all()

    def get_serializer_class(self):
        req = self.request
        if req.method in ['PATCH', 'PUT']:
            return serializers.CategorySerializer4AdminUpdate
        if is_it_admin(req) or is_it_its(req, CityAdmin):
            return serializers.CategorySerializer4Admin
        if is_it_its(req, Employee):
            pk = self.kwargs.get('pk')
            employee = get_my_object(req, Employee)
            category = get_object_or_404(models.Category, pk=pk)
            if employee.expert and employee.expert.category == category:
                return serializers.CategorySerializer4Admin
            if employee in category.employees.all():
                return serializers.CategorySerializer4Admin
            return serializers.CategorySerializerReadOnly
        return serializers.CategorySerializerReadOnly


class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = models.Province.objects.all()
    serializer_class = serializers.ProvinceSerializer
    # ? Admin or ReadOnly
    permission_classes = [AdminPermission | ReadOnly]


class CityViewSet(viewsets.ModelViewSet):
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer
    # ? Admin or ReadOnly
    permission_classes = [AdminPermission | ReadOnly]


class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = models.TimeTable.objects.all()
    serializer_class = serializers.TimeTableSerializer
    permission_classes = [AdminPermission | ReadOnly]


class TimeTableVisitorList(generics.ListCreateAPIView):
    permission_classes = [(CustomerPermission & ReadOnly) | VisitorPermission |
                          AdminPermission | CityAdminPermission]
    queryset = TimeTableVisitor.objects.all()

    def get_queryset(self):
        if is_it_admin(self.request):
            return self.queryset
        elif is_it_its(self.request, Visitor):
            return self.queryset.filter(
                visitor=get_my_object(self.request, Visitor))
        elif is_it_its(self.request, CityAdmin):
            return self.queryset.filter(
                visitor__city=get_my_object(self.request, CityAdmin).city)
        elif is_it_its(self.request, Customer):
            return self.queryset.filter(Q(
                project__customer=get_my_object(self.request, Customer)) | Q(project__isnull=True))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            print('post method')
            return serializers.TimeTableVisitorSerializerCreate
        else:
            return serializers.TimeTableVisitorSerializer

    def perform_create(self, serializer):
        if is_it_its(self.request, Visitor):
            visitor = get_my_object(self.request, Visitor)
            return serializer.save(visitor=visitor)
        return super().perform_create(serializer)


class TimeTableVisitorDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TimeTableVisitorSerializer
    permission_classes = [CustomerPermission | (VisitorPermission & ReadOnly) |
                          AdminPermission | CityAdminPermission]

    def get_queryset(self):
        if is_it_admin(self.request):
            return TimeTableVisitor.objects.all()
        elif is_it_its(self.request, Visitor):
            return TimeTableVisitor.objects.filter(
                visitor=get_my_object(self.request, Visitor))
        elif is_it_its(self.request, CityAdmin):
            return TimeTableVisitor.objects.filter(
                visitor__city=get_my_object(self.request, CityAdmin).city)
        elif is_it_its(self.request, Customer):
            return TimeTableVisitor.objects.filter(Q(
                project__customer=get_my_object(self.request, Customer)) | Q(project__isnull=True))

    def get_serializer_class(self):
        req = self.request
        if req.method in ['PUT', 'PATCH']:
            if is_it_its(req, Customer):
                return serializers.TimeTableVisitorSerializerUpdate4Customer
        return serializers.TimeTableVisitorSerializer

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [AdminPermission | CityAdminPermission]
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        if is_it_its(self.request, Customer):
            project = serializer.validated_data.get('project')
            if project.customer == get_my_object(self.request, Customer):
                return super().perform_update(serializer)
            else:
                raise ValidationError(
                    {'project': 'this project does not belong to you'})
        else:
            return super().perform_update(serializer)


class ReportEmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.ReportEmployee.objects.all()
    serializer_class = serializers.ReportEmployeeSerializer4admin
    permission_classes = [AdminPermission | CityAdminPermission |
                          (ExpertPermission & CreateRead) | (CustomerPermission & CreateRead)]

    def get_queryset(self):
        req = self.request
        if is_it_expert(req):
            return models.ReportEmployee.objects.filter(rep_expert=get_my_expert(req))
        elif is_it_its(req, Customer):
            return models.ReportEmployee.objects.filter(rep_customer=get_my_object(req, Customer))
        elif is_it_its(req, CityAdmin):
            return models.ReportEmployee.objects.filter(project__city=get_my_object(req, CityAdmin).city)
        elif is_it_admin(req):
            return super().get_queryset()

    def perform_create(self, serializer):
        employee = serializer.validated_data.get('employee')
        project = serializer.validated_data.get('project')
        req = self.request
        # Validation
        if employee in project.employees.all():
            if is_it_expert(req):
                expert = get_my_expert(self.request)
                verifyexpert = get_object_or_404(
                    VerifyExpert, expert=expert, project=project)
                if verifyexpert is not None:
                    srsave = serializer.save(rep_expert=get_my_expert(req))
            elif is_it_its(req, Customer):
                cust = get_my_object(req, Customer)
                if project.customer == cust:
                    srsave = serializer.save(
                        rep_customer=cust)
            elif is_it_its(req, CityAdmin):
                cd = get_my_object(req, CityAdmin)
                if project.city == cd.city:
                    srsave = serializer.save(
                        rep_cd=cd)
            elif is_it_admin(req):
                srsave = serializer.save()

            if srsave != None:
                if project.status == 'doing':
                    project.status = 'stopped'
                    project.save()
                    project.timer.time = timezone.now()
                    project.timer.save()

                return srsave
        else:
            raise ValidationError('The employee is not in this project')


class CompanyInfoViewSet(viewsets.ModelViewSet):
    queryset = models.CompanyInfo.objects.all()
    serializer_class = serializers.CompanyInfoSerializer
    permission_classes = [AdminPermission | ReadOnly]

    def perform_create(self, serializer):
        try:
            models.CompanyInfo.objects.get(id=1)
        except:
            return super().perform_create(serializer)
        raise exceptions.ValidationError(
            {'Unique': 'This object is already available'})
