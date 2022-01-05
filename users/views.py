from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from users.serializers import EmployeeSerializer, VisitorSerializer
from authentication.utils import get_my_object
from itapi.models import Category
from itapi.serializers import CategorySerializerReadOnly
from users.models import Commis, Employee, CityAdmin
from rest_framework.views import APIView
from authentication.permission import AdminPermission, CityAdminPermission, EmployeePermission, EmployeePermissionUnapproved, ReadOnly, VisitorPermission, VisitorPermissionUnapproved
from rest_framework import exceptions
from authentication.utils import get_my_object, is_it_admin, is_it_its
from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics, viewsets
from users.serializers import Admin_Resume_Serializer, CityAdminSerializer, CommisSerializer, ExpertSerializer, ExpertSerializerUpdate, \
    Resume_Serializer
from users.models import Employee, Expert, Resume, Visitor, CityAdmin


class CategoryEmployee(ListAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        """Get City Employees"""
        cityAdmin = get_my_object(self.request, CityAdmin)
        city = cityAdmin.city
        employees = city.employee.all()
        return employees


class UserResume(mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = Resume.objects.all()
    serializer_class = Resume_Serializer
    permission_classes = [VisitorPermissionUnapproved |
                          EmployeePermissionUnapproved]

    def get_object(self):
        if self.kwargs["type"] == "employee":
            user = get_my_object(self.request, Employee)
            obj = get_object_or_404(Resume, employee=user)

        elif self.kwargs["type"] == "visitor":
            user = get_my_object(self.request, Visitor)
            obj = get_object_or_404(Resume, visitor=user)

        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        obj = serializer.save(status="ns", reason="")

    def perform_create(self, serializer):

        if self.kwargs["type"] == "employee":
            user = get_my_object(self.request, Employee)
        elif self.kwargs["type"] == "visitor":
            user = get_my_object(self.request, Visitor)

        if user.resume == None:
            # ? create resume obj :
            new_resume = serializer.save()
            # ? connect user to resume obj :
            user.resume = new_resume
            user.save()
        else:
            raise exceptions.ValidationError(
                detail="resume is available", code=400)


class CheckResume(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Resume.objects.all()
    serializer_class = Admin_Resume_Serializer
    permission_classes = [AdminPermission | CityAdminPermission]

    def get_queryset(self):
        if is_it_its(self.request, CityAdmin):
            my_city_admin = get_my_object(self.request, CityAdmin)
            if self.request.body["type"] == "employee":
                return Resume.objects.filter(employee_city=my_city_admin.city)
            elif self.request.body["type"] == "visitor":
                return Resume.objects.filter(visitor_city=my_city_admin.city)
            else:
                return None
        elif is_it_admin(self.request):
            return Resume.objects.all()
        else:
            return None

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        if serializer.validated_data['status'] == 'ap':
            obj = self.get_object()
            if Employee.objects.filter(resume=obj).exists():
                obj.employee.approved = True
                obj.employee.save()
            elif Visitor.objects.filter(resume=obj).exists():
                obj.visitor.approved = True
                obj.visitor.save()
            else:
                return None
            serializer.save()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AllResume(generics.ListAPIView):
    queryset = Resume.objects.all()
    serializer_class = Admin_Resume_Serializer
    permission_classes = [AdminPermission | CityAdminPermission]
    filterset_fields = ['status', ]

    def get_queryset(self):
        if is_it_its(self.request, CityAdmin):
            my_city_admin = get_my_object(self.request, CityAdmin)
            if self.kwargs["type"] == "employee":
                return Resume.objects.filter(employee_city=my_city_admin.city)
            elif self.kwargs["type"] == "visitor":
                return Resume.objects.filter(visitor_city=my_city_admin.city)
            else:
                return None
        elif is_it_admin(self.request):
            return Resume.objects.all()
        else:
            return None


class CityAdminViewSet(viewsets.ModelViewSet):
    queryset = CityAdmin.objects.all()
    serializer_class = CityAdminSerializer
    permission_classes = [AdminPermission, ]

    def create(self, request, *args, **kwargs):
        raise exceptions.NotAcceptable()


class EmployeesViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [(AdminPermission) | (CityAdminPermission & ReadOnly)]
    queryset = Employee.objects.all()
    filterset_fields = ['approved', 'city', ]

    def get_queryset(self):
        if is_it_its(self.request, CityAdmin):
            cityAdmin = get_my_object(self.request, CityAdmin)
            city = cityAdmin.city
            employees = city.employee.all()
            return employees
        elif is_it_admin(self.request):
            return self.queryset
        else:
            raise NotFound


class ExpertsViewSet(viewsets.ModelViewSet):
    permission_classes = [(AdminPermission) | (CityAdminPermission & ReadOnly)]
    queryset = Expert.objects.all()

    def get_queryset(self):
        if is_it_its(self.request, CityAdmin):
            cityAdmin = get_my_object(self.request, CityAdmin)
            exports = self.queryset.filter(employee__city=cityAdmin.city)
            return exports
        elif is_it_admin(self.request):
            return self.queryset
        else:
            raise NotFound

    def get_serializer_class(self):
        req = self.request
        if req.method in ['PATCH', 'PUT']:
            return ExpertSerializerUpdate
        else:
            return ExpertSerializer

    def perform_create(self, serializer):
        if is_it_admin(self.request):
            return serializer.save()
        elif is_it_its(self.request, CityAdmin):
            emp = serializer.validated_data.get('employee')
            cityadmin = get_my_object(self.request, CityAdmin)
            if emp.city == cityadmin.city:
                return serializer.save()
            else:
                return exceptions.ValidationError({'You cannot do this.'})


class VisitorsViewSet(viewsets.ModelViewSet):
    serializer_class = VisitorSerializer
    permission_classes = [(AdminPermission) | ReadOnly]
    queryset = Visitor.objects.all()
    filterset_fields = ['approved', 'city', ]

    def get_queryset(self):
        if is_it_its(self.request, CityAdmin):
            cityAdmin = get_my_object(self.request, CityAdmin)
            exports = self.queryset.filter(city=cityAdmin.city)
            return exports
        elif is_it_admin(self.request):
            return self.queryset
        else:
            raise NotFound


class AddEmployee2Category(APIView):
    def post(self, request, *args, **kwargs):
        category = get_object_or_404(Category, id=kwargs['pk'])
        if request.data and 'employee' in request.data:
            employee = get_object_or_404(Employee, id=request.data['employee'])
            if is_it_its(request, CityAdmin):
                if get_my_object(request, CityAdmin).city == employee.city:
                    if employee in category.employees.all():
                        category.employees.remove(employee)
                    else:
                        category.employees.add(employee)
                else:
                    raise ValidationError('access denied!')
            elif is_it_admin(request):
                if employee in category.employees.all():
                    category.employees.remove(employee)
                else:
                    category.employees.add(employee)
            else:
                raise NotFound
        else:
            raise ValidationError('There is no data in body')
        return Response(CategorySerializerReadOnly(category).data)


class CommisViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Commis.objects.all()
    serializer_class = CommisSerializer
    permission_classes = [AdminPermission | (
        (VisitorPermission | CityAdminPermission) & ReadOnly)]

    def perform_create(self, serializer):
        try:
            Commis.objects.get(id=1)
        except:
            return super().perform_create(serializer)
        raise exceptions.ValidationError(
            {'Unique': 'This object is already available'})
