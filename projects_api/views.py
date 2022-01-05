from rest_framework.exceptions import NotFound
from datetime import timedelta
from rest_framework import generics, mixins, viewsets
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from rest_framework import exceptions, generics, mixins
from projects_api.permissions import CityAdminInProject, EmployeeInProject, ExpertInProject, ExpertIsOwnerEmp, \
    ExpertTopInProject, ExpertTopPermission, ProjectCustomerOwner
from projects_api.serializers import *
from .models import *
from authentication.permission import AdminPermission, CityAdminPermission, CustomerPermission, EmployeePermission, \
    ExpertPermission, ReadOnly, VisitorPermission
from authentication.utils import get_my_expert, get_my_object, get_token, get_wallet, get_wallet_without_verify, \
    is_it_admin, is_it_expert, is_it_its, send_request_to_server
from wallet_part.utils import create_part, create_part_data, spend_from_part, spend_part_data
from rest_framework import generics, mixins

from mail.utils import SendCustomPostRequest2Mail
from projects_api.serializers import *
from .models import *
from authentication.permission import AdminPermission, CustomerPermission, EmployeePermission, ReadOnly, \
    VisitorPermission
from authentication.utils import get_my_object, get_token, get_wallet, get_wallet_without_verify, is_it_admin, \
    is_it_its, get_my_expert
from wallet_part.utils import create_part, create_part_data
from users.models import CityAdmin, Customer, Employee, Expert, Visitor
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from projects_api.utils import is_project_experts_approve, is_project_owner
from django.db.models import Count
from projects_api.models import Project, ProjectRequestEmployee, VerifyExpert
from decouple import config
from django.utils import timezone

# * Server Information :
HOST_WALLET = config('HOST_WALLET')
TOKEN = config('TOKEN')
PART_URL = HOST_WALLET + "/part/"

MAIL_HOST = config('MAIL_HOST')


class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectCreate
    # todo only employees, experts and admins can access readonly and customer create
    permission_classes = []

    def get_queryset(self):
        request = self.request
        if is_it_admin(request):
            return Project.objects.all()
        elif is_it_its(request, Customer):
            customer = get_my_object(request, Customer)
            return Project.objects.filter(customer=customer)
        elif is_it_its(request, Employee):
            employee = get_my_object(request, Employee)
            return Project.objects.filter(
                employees__in=[employee])
        elif is_it_its(request, CityAdmin):
            # ? if it is cityadmin
            cityadmin = get_my_object(request, CityAdmin)
            return Project.objects.filter(city=cityadmin.city)
        elif is_it_its(request, Visitor):
            visitor = get_my_object(request, Visitor)
            return Project.objects.filter(visitor=visitor)
        # todo query for Expert
        elif is_it_expert(request):
            return Project.objects.filter(verifies__expert=get_my_expert(request))
        else:
            raise PermissionDenied()

    def get(self, request, *args, **kwargs):
        self.serializer_class = ProjectRead
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # permission classes
        self.permission_classes = [AdminPermission | CustomerPermission]
        self.serializer_class = ProjectCreate
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        customer = get_my_object(self.request, Customer)
        # todo create the first verifyexpert(it is created with signals)
        serializer.save(customer=customer)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectRead4CustomerOwner
    # todo employees and experts and customer and admincity can access
    permission_classes = [(AdminPermission) |
                          (CityAdminPermission & CityAdminInProject) |
                          (EmployeePermission & EmployeeInProject & ReadOnly) |
                          (ExpertPermission & ExpertInProject & ReadOnly) |
                          (ExpertTopPermission & ExpertTopInProject) |
                          (CustomerPermission & ProjectCustomerOwner & ReadOnly)]

    def get_serializer_class(self):
        req = self.request
        if req.method == "GET":
            return super().get_serializer_class()
        elif req.method in ['PUT', 'PATCH']:
            if is_it_admin(req):
                return ProjectRead4CustomerOwner
            elif is_it_its(req, Customer):
                obj = self.get_object()
                if obj.experts_approve:
                    raise exceptions.PermissionDenied(
                        'Project has already started')
                else:
                    # delete all verify Experts
                    return ProjectUpdate4CustomerOwner
            elif is_it_expert(req):
                return ProjectUpdate4TopExpert

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [(AdminPermission) |
                                   (CityAdmin & CityAdminInProject) |
                                   (ExpertTopPermission & ExpertTopInProject)]
        return super().delete(request, *args, **kwargs)

    def perform_update(self, serializer):
        req = self.request
        # obj = self.get_object()
        obj = get_object_or_404(Project, id=self.kwargs['pk'])
        status = serializer.validated_data.get('status')
        # check status
        if obj.status == 'doing' and status == 'stopped':
            obj.timer.time = timezone.now()
            obj.timer.save()
        elif obj.status == 'stopped' and status == 'doing':
            time_exper = obj.time_expert + \
                timedelta(days=(timezone.now() - obj.timer.time).days)
            # (timezone.now() - obj.timer.time).days
            return serializer.save(time_expert=time_exper)
        elif status == 'done' and obj.status == 'stopped':
            raise ValidationError(
                {'status': 'You cannot do this first you have change status to doing then change it to done'})
        elif status == 'done' and obj.status == 'doing':
            # pay commissions
            project = self.get_object()
            all_part = Parts.objects.filter(project=project)
            project_employee = project.employees
            project_cityadmin = project.city.city_admin
            project_vfs = project.verifies.all()
            if timezone.now() <= project.time_expert:
                days = 0
            else:
                delay = timezone.now() - project.time_expert
                days = delay.days
            for part in all_part:
                section = []
                for category in project.categories.all():
                    emps = project_employee.filter(
                        category__parent=category)
                    level_cat = category.get_level()
                    if project_vfs.filter(category__level=level_cat).count() > 1:
                        commission = category.commission_employee2
                    else:
                        commission = category.commission_employee1

                    com = (commission / emps.count()) - \
                          (category.penalty * days)
                    for emp in emps:
                        new = {
                            "wallet_id": emp.wallet.id,
                            "percent": com
                        }
                        emp.yellow_cards = emp.yellow_cards + int(days)
                        emp.save()
                        section.append(new)
                for vf in project_vfs:
                    level_vf = vf.category.get_level()
                    if project_vfs.filter(category__level=level_vf).count() > 1:
                        commission = vf.category.commission2
                    else:
                        commission = vf.category.commission1
                    new = {
                        "wallet_id": vf.expert.employee.wallet.id,
                        "percent": vf.category.commission1 - (vf.category.penalty * days)
                    }
                    ex = vf.expert
                    ex.yellow_cards = ex.yellow_cards + days
                    ex.save()
                    section.append(new)
                from users.models import Commis
                commis_id = get_object_or_404(Commis, id=1)
                if project.visitor:
                    new = {
                        "wallet_id": project.visitor.wallet.id,
                        "percent": commis_id.visitor
                    }
                    section.append(new)
                if project_cityadmin:
                    new = {
                        "wallet_id": project.project_cityadmin.wallet.id,
                        "percent": commis_id.cityadmin
                    }
                    section.append(new)

                data_spend_from_part = spend_part_data(
                    amount=project.price_expert, section=section)
                response = spend_from_part(
                    part_id=part.id, data=data_spend_from_part)

        if is_it_its(req, Customer):
            return serializer.save(experts_approve=False)
        else:
            return serializer.save()


class PrpjectPrePrice(APIView):
    permission_classes = [CustomerPermission]

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['project_id'])
        buy_type = kwargs['buy_type']
        wallet = get_wallet_without_verify(request)
        is_project_owner(project, wallet)
        is_project_experts_approve(project)

        pre_price = project.pre_price
        data_create_part = create_part_data(wallet.id, amount=pre_price)
        part_id = create_part(data=data_create_part)

        project.pre_price_paid == True
        part = Parts.objects.create(id=part_id, project=project)
        project.part.add(part)
        project.save()

        top_expert_vf = project.verifies.filter(expert__category__parent=None)
        emps = top_expert_vf.empcounts.all()

        if project.need_visitor == True:
            visitor = Visitor.objects.filter(
                city=project.city).annotate(num_projects=Count('projects')) \
                .order_by('num_projects')
            new_project_request_obj = ProjectRequestVisitor.objects.create(
                active_visitor=visitor[0], project=project, city=project.city)
            new_project_request_obj.visitor.add(*visitor)
            for emp in emps:
                employee = Employee.objects.filter(
                    categories__in=[emp.attrib], city=project.city).annotate(num_projects=Count('projects')) \
                    .order_by('num_projects', 'yellow_cards')
                new_project_request_obj = ProjectRequestEmployee.objects.create(
                    project=project, category=emp.attrib, pointer=emp.count)
                new_project_request_obj.active_employee.add(
                    *employee[emp.count:])
                new_project_request_obj.employee.add(*employee[:emp.count])
        else:
            for emp in emps:
                employee = Employee.objects.filter(
                    categories__in=[emp.attrib]).annotate(num_projects=Count('projects')) \
                    .order_by('num_projects', 'yellow_cards')
                new_project_request_obj = ProjectRequestEmployee.objects.create(
                    project=project, category=emp.attrib, pointer=emp.count)
                new_project_request_obj.active_employee.add(
                    *employee[emp.count:])
                new_project_request_obj.employee.add(*employee[:emp.count])

        Timer.objects.create(project=project)
        return Response(data="finish", status=200)


class EmployeeProjectDo(APIView):
    permission_classes = [EmployeePermission]

    def get(self, request, *args, **kwargs):
        employee = get_my_object(request, Employee)
        result = kwargs["result"]
        project_request = get_object_or_404(
            ProjectRequestEmployee, id=kwargs["request_id"], active_employee=employee)

        project_request.action(result, employee)

        return Response("finish", status=200)


class VisitorProjectDo(APIView):
    permission_classes = [VisitorPermission]

    def get(self, request, *args, **kwargs):
        visitor = get_my_object(request, Visitor)
        result = kwargs["result"]
        project_request = get_object_or_404(
            ProjectRequestVisitor, id=kwargs["request_id"], active_visitor=visitor)

        project_request.action(result, visitor)

        return Response("finish", status=200)


class VerifyExpertAPI(generics.RetrieveUpdateAPIView):
    serializer_class = VerifyExpertSerializer
    queryset = VerifyExpert

    def get(self, request, *args, **kwargs):
        """Get Verify Expert"""
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Update Verify Expert"""
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        expert = get_my_expert(self.request)
        verifyExpert = self.get_object()
        if verifyExpert.status == 'ns':
            if verifyExpert.project.visitor:
                if verifyExpert.category == expert.category and expert.city == expert.city:
                    UnVerified = []
                    for i in VerifyExpert.objects.filter(project=verifyExpert.project,
                                                         category__in=verifyExpert.category.subcategories.all()):
                        if i.status != 'ok':
                            UnVerified.append(i)
                    if not UnVerified:

                        if not verifyExpert.category.parent:
                            SendCustomPostRequest2Mail(request=self.request,
                                                       data={'name': verifyExpert.project.name,
                                                             'users': verifyExpert.project.customer.wallet.id,
                                                             'admin': expert.employee.city.city_admin, 'type': 'G'},
                                                       link=f'{MAIL_HOST}/chat/')
                        return serializer.save(category=verifyExpert.category, project=verifyExpert.project,
                                               expert=expert)
                    else:
                        raise ValidationError(
                            'please verify lowrance category')
                else:
                    raise ValidationError('access denied!')
            else:
                if verifyExpert.category == expert.category:
                    UnVerified = []
                    for i in VerifyExpert.objects.filter(project=verifyExpert.project,
                                                         category__in=verifyExpert.category.subcategories.all()):
                        if i.status != 'ok':
                            UnVerified.append(i)
                    if not UnVerified:
                        if not verifyExpert.category.parent:
                            SendCustomPostRequest2Mail(request=self.request,
                                                       data={'name': verifyExpert.project.name,
                                                             'users': verifyExpert.project.customer.wallet.id,
                                                             'admin': expert.employee.city.city_admin, 'type': 'G'},
                                                       link=f'{MAIL_HOST}/chat/')
                        return serializer.save(category=verifyExpert.category, project=verifyExpert.project,
                                               expert=expert)
                    else:
                        raise ValidationError(
                            'please verify lowrance category')
                else:
                    raise ValidationError('access denied!')
        else:
            raise ValidationError("You've verified this before!")


class VerifyExpertViewSet(viewsets.ModelViewSet):
    queryset = VerifyExpert.objects.all()
    serializer_class = VerifyExpertSerializer
    permission_classes = [AdminPermission]


class ListProjectVerifyExpert(ListAPIView):
    serializer_class = VerifyExpertSerializer

    def get_queryset(self):
        """Get Project's Verify Expert"""
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        verifyExperts = project.verifies.all()
        return verifyExperts


class ListVerifyExperts(ListAPIView):
    serializer_class = VerifyExpertSerializer

    def get_queryset(self):
        if is_it_expert(self.request):
            return VerifyExpert.objects.filter(category=get_my_expert(self.request).category)
        elif is_it_admin(self.request):
            return VerifyExpert.objects.all()
        else:
            raise NotFound


class PayDateTimeList(generics.ListCreateAPIView):
    # todo permission only top expert can create
    permission_classes = [ExpertTopPermission | AdminPermission | CityAdminPermission | (
        (ExpertPermission | CustomerPermission) & ReadOnly)]
    serializer_class = PayDateTimeSerializer

    def get_queryset(self):
        req = self.request
        if is_it_expert(req):
            expert = get_my_object(req, Expert)
            return PayDateTime.objects.filter(project__city=expert.city)
        elif is_it_its(req, CityAdmin):
            cityadmin = get_my_object(req, CityAdmin)
            return PayDateTime.objects.filter(project__city=cityadmin.city)
        elif is_it_its(req, Customer):
            customer = get_my_object(req, Customer)
            return PayDateTime.objects.filter(project__customer=customer)
        else:
            # if admin
            return PayDateTime.objects.all()

    def perform_create(self, serializer):
        if is_it_expert(self.request):
            expert = get_my_expert(self.request)
            project = serializer.validated_data.get('project')
            if VerifyExpert.objects.filter(project=project, expert=expert).exists():
                return super().perform_create(serializer)
            else:
                raise ValidationError('You do not have access to this project')
        else:
            return super().perform_create(serializer)


class PayDateTimeDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission classes for get request
    permission_classes = [ExpertTopPermission |
                          AdminPermission | CityAdminPermission | ReadOnly]
    serializer_class = PayDateTimeSerializer

    def get_queryset(self):
        req = self.request
        if is_it_expert(req):
            expert = get_my_object(req, Expert)
            return PayDateTime.objects.all()
        elif is_it_its(req, CityAdmin):
            cityadmin = get_my_object(req, CityAdmin)
            return PayDateTime.objects.filter(project__city=cityadmin.city)
        elif is_it_its(req, Customer):
            customer = get_my_object(req, Customer)
            return PayDateTime.objects.filter(project__customer=customer)
        else:
            # if admin
            return PayDateTime.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return PayDateTimeSerializerUpdate
        return super().get_serializer_class()

    def put(self, request, *args, **kwargs):
        paydatetime = self.get_object()
        if paydatetime.paid:
            raise exceptions.PermissionDenied('This check has been paid.')
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        paydatetime = self.get_object()
        if paydatetime.paid:
            raise exceptions.PermissionDenied('This check has been paid.')
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # todo permission classes
        self.permission_classes = []
        return super().delete(request, *args, **kwargs)


class PayDateTimePay(APIView):
    permission_classes = [CustomerPermission]

    def get(self, request, *args, **kwargs):
        try:
            paydatetime = kwargs['pk']
            wallet = get_wallet_without_verify(request)
            obj = get_object_or_404(
                PayDateTime, id=paydatetime, project__customer__wallet=wallet)
        except:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)
        if obj.paid == True:
            raise exceptions.ValidationError(
                detail="Already paid", code=400)
        data_create_part = create_part_data(
            wallet_id=obj.project.customer.wallet.id, amount=obj.amount)
        part_id = create_part(data_create_part)
        part = Parts.objects.create(id=part_id, project=obj.project)
        obj.paid = True
        obj.save()
        return Response("Payment is done", status=200)


class ReMoney(APIView):
    permission_classes = [CityAdminPermission]

    def get(self, request, *args, **kwargs):
        try:
            user = get_my_object(request, CityAdmin)
            project_pk = kwargs['project_id']
            project = get_object_or_404(
                Project, id=project_pk)
            get_object_or_404(CityAdmin, city=project.city)

        except:
            raise exceptions.ValidationError(
                detail="Invalid data", code=400)

        from decouple import config
        HOST_WALLET = config('HOST_WALLET')
        TOKEN = config('TOKEN')
        TRANSACTION_URL = HOST_WALLET + "/transaction/"

        all_part = Parts.objects.filter(project=project)
        for part in all_part:
            url = TRANSACTION_URL + str(part.id) + "/reject"
            token = TOKEN
            send_request_to_server(url=url, request_type="post", token=token)

        return Response("ok", status=200)


class EmpCountList(generics.ListCreateAPIView):
    serializer_class = EmployeeCountSerializer
    permission_classes = [(ExpertPermission) |
                          (CityAdminPermission) |
                          (AdminPermission)]

    def get_queryset(self):
        req = self.request
        if req.method == "GET":
            if is_it_admin(req):
                return EmployeeCount.objects.all()
            elif is_it_its(req, CityAdmin):
                cd = get_my_object(req, CityAdmin)
                return EmployeeCount.objects.filter(ve__project__city=cd.city)
            elif is_it_expert(req):
                ex = get_my_object(req, Expert)
                return EmployeeCount.objects.all()
            return None

    def perform_create(self, serializer):
        # Validate VerifyExpert
        if is_it_expert(self.request):
            ex = get_my_expert(self.request)
            ve = serializer.validated_data.get('ve')
            if ve.expert == ex:
                return super().perform_create(serializer)
            raise ValidationError(
                'You cannot create employee Count for this verify')
        else:
            return super().perform_create(serializer)


class EmpCountDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [(ExpertPermission & ExpertIsOwnerEmp) |
                          (ExpertPermission & ReadOnly) |
                          (AdminPermission) |
                          (CityAdminPermission)]

    def get_queryset(self):
        req = self.request
        if is_it_admin(req):
            return EmployeeCount.objects.all()
        elif is_it_its(req, CityAdmin):
            cd = get_my_object(req, CityAdmin)
            return EmployeeCount.objects.filter(ve__project__city=cd.city)
        elif is_it_expert(req):
            ex = get_my_object(req, Expert)
            return EmployeeCount.objects.all()
        return None

    def get_serializer_class(self):
        req = self.request
        if req.method in ['PUT', 'PATCH']:
            return EmployeeCountSerializerUpdate
        else:
            return EmployeeCountSerializer


class PartCityAdmin(generics.GenericAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin):
    permission_classes = [CityAdminPermission]
    serializer_class = PartSerializer
    lookup_field = "id"

    def get_queryset(self):
        req = self.request
        user = get_my_object(req, CityAdmin)
        return Parts.objects.filter(project__city=user.city)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        part_id = self.kwargs[self.lookup_field]
        try:
            obj = get_object_or_404(queryset, id=part_id)
        except:
            raise exceptions.ValidationError(
                detail="cant found obj", code=400)
        return obj

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        obj = instance
        token = get_token(self.request)
        url = PART_URL + str(obj.id)
        # instance.delete()
        return send_request_to_server(url, "delete", token=TOKEN)


class PartCustomer(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [CustomerPermission]
    serializer_class = PartSerializer

    def get_queryset(self):
        req = self.request
        user = get_my_object(req, Customer)
        return Parts.objects.filter(project__customer=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StartChatBetweenExpertAndEmployees(APIView):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['pk'])
        expert = get_my_expert(request)
        if not expert.category.parent:
            try:
                project.verifies.get(expert=expert, status='ok')
                if project.pre_price_paid:
                    return SendCustomPostRequest2Mail(request,
                                                      data={'name': project.name,
                                                            'users': list(project.employees.all()),
                                                            'type': 'G'},
                                                      link=f'{MAIL_HOST}/chat/')
                else:
                    raise ValidationError('Pre price did not paid!')
            except VerifyExpert.DoesNotExist:
                raise ValidationError('access denied!')
        else:
            raise ValidationError('access denied!')
