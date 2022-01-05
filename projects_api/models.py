from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed, pre_save

from rest_framework import exceptions
from users.models import Employee, Visitor
from django.db.models import Count


class Parts(models.Model):
    id = models.CharField(max_length=80, primary_key=True)
    project = models.ForeignKey(
        'Project',
        related_name='part',
        on_delete=models.CASCADE,
        null=True,
        blank=True)


class Project(models.Model):
    STATUS_CHOICES = [
        ('not_approved', 'تایید نشده'),
        ('not_started', 'شروع نشده'),
        ('doing', 'درحال انجام'),
        ('done', 'انجام شد'),
        ('stopped', 'متوقف شده')
    ]

    created_time = models.DateTimeField(auto_now_add=True)
    # customer fields
    name = models.CharField(max_length=80)
    customer_deadline = models.DateTimeField()
    customer_description = models.TextField(blank=True)
    file = models.FileField(blank=True)
    customer_approve = models.BooleanField(default=False)
    categories = models.ManyToManyField(
        'itapi.Category',
        related_name='projects', )
    customer_price = models.PositiveIntegerField(blank=True, null=True)
    customer = models.ForeignKey(
        'users.Customer',
        related_name='projects',
        on_delete=models.CASCADE,
        null=True)
    city = models.ForeignKey(
        'itapi.City',
        related_name='projects',
        on_delete=models.PROTECT,
        null=True,
        blank=True)

    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=15,
        default="not_approved")
    employees = models.ManyToManyField(
        'users.Employee',
        blank=True,
        related_name='projects')
    price_paid = models.BooleanField(default=False)
    paid_money = models.PositiveIntegerField(default=0)
    pre_price_paid = models.BooleanField(default=False,
                                         null=True)
    pre_price = models.PositiveIntegerField(blank=True,
                                            null=True)
    need_visitor = models.BooleanField(default=False)
    visitor = models.ForeignKey(
        'users.Visitor',
        blank=True,
        null=True,
        related_name='projects',
        on_delete=models.PROTECT)

    experts_approve = models.BooleanField(default=False)
    # inherit from verifyexpert
    price_expert = models.PositiveBigIntegerField(null=True, blank=True)
    time_expert = models.DateTimeField(null=True, blank=True)
    description_expert = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class PayDateTime(models.Model):
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='paytimes',
                                null=True,
                                blank=True)
    deadline = models.DateTimeField()
    amount = models.PositiveBigIntegerField()
    paid = models.BooleanField(default=False)


class VerifyExpert(models.Model):
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='verifies')
    category = models.ForeignKey('itapi.Category',
                                 on_delete=models.CASCADE,
                                 related_name='categories')
    expert = models.ForeignKey('users.Expert',
                               blank=True,
                               null=True,
                               on_delete=models.CASCADE,
                               related_name='verifies')
    STATUS_CHOICES = [
        ('ns', 'not seen'),
        ('ok', 'ok'),
        ('nk', 'not ok'),
    ]
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=3,
                              default='ns')

    count = models.PositiveSmallIntegerField(blank=True, null=True)
    salary = models.PositiveBigIntegerField(blank=True, null=True)
    time = models.DurationField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class ProjectRequestEmployee(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    pointer = models.IntegerField(default=1)
    active_employee = models.ManyToManyField(
        'users.Employee', related_name="projectrequests")
    employee = models.ManyToManyField(
        'users.Employee')
    category = models.ForeignKey('itapi.Category', on_delete=models.CASCADE)

    class Meta:
        ordering = ('employee__yellow_cards',)

    def action(self, result, employee):
        if result == "accept":
            self.project.employees.add(employee)
            self.employee.remove(employee)

        elif result == "reject":
            if self.employee == None:
                top_expert_vf = self.project.verifies.filter(
                    expert__category__parent=None)
                emps = top_expert_vf.empcounts.all()

                if self.project.need_visitor == True:

                    for emp in emps:
                        employee = Employee.objects.filter(
                            categories__in=[emp.attrib], city=self.project.city).annotate(
                            num_projects=Count('projects')) \
                            .order_by('num_projects', 'yellow_cards')
                        employee = employee.exclude(
                            projects__in=[self.project])
                        new_project_request_obj = ProjectRequestEmployee.objects.create(
                            project=self.project, category=emp.attrib)
                        new_project_request_obj.active_employee.add(
                            *employee[self.pointer:])
                        new_project_request_obj.employee.add(
                            *employee[:self.pointer])
                else:
                    for emp in emps:
                        employee = Employee.objects.filter(
                            categories__in=[emp.attrib]).annotate(num_projects=Count('projects')) \
                            .order_by('num_projects', 'yellow_cards')
                        employee = employee.exclude(
                            projects__in=[self.project])
                        new_project_request_obj = ProjectRequestEmployee.objects.create(
                            project=self.project, category=emp.attrib)
                        new_project_request_obj.active_employee.add(
                            *employee[self.pointer:])
                        new_project_request_obj.employee.add(
                            *employee[:self.pointer])

            else:
                self.active_employee.remove(employee)
                self.active_employee.add(employee[0])
                self.employee.remove(self.employee[0])
                self.save()

        else:
            raise exceptions.ValidationError(detail="Invalid result", code=400)


class ProjectRequestVisitor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    active_visitor = models.ForeignKey(
        'users.Visitor', on_delete=models.CASCADE, related_name="projectrequests")
    visitor = models.ManyToManyField('users.Visitor')
    city = models.OneToOneField('itapi.City', on_delete=models.CASCADE)

    def action(self, result, visitor):
        if result == "accept":
            self.project.visitor.add(visitor)
            self.delete()

        elif result == "reject":
            if self.visitor == None:
                visitor = Visitor.objects.filter(
                    city=self.city).annotate(num_projects=Count('projects')) \
                    .order_by('num_projects', 'yellow_cards')
                self.active_visitor = visitor[0]
                self.visitor.add(*visitor)
            else:
                self.visitor.remove(visitor)
                self.active_visitor = self.visitor[0]
                self.save()

        else:
            raise exceptions.ValidationError(detail="Invalid result", code=400)


def validate_attrib(value):
    if value.subcategories:
        return ValidationError({'category': 'is not attrib(last level)'})


class EmployeeCount(models.Model):
    ve = models.ForeignKey(VerifyExpert,
                           on_delete=models.CASCADE,
                           related_name='empcounts')
    attrib = models.ForeignKey('itapi.Category',
                               on_delete=models.CASCADE,
                               related_name='empcounts',
                               validators=[validate_attrib])
    count = models.PositiveSmallIntegerField()


class Timer(models.Model):
    time = models.DateTimeField(default=None)
    project = models.OneToOneField(Project,
                                   on_delete=models.CASCADE,
                                   related_name='timer')


# Creating verifyExpert
def ProjectCategorym2m_change(sender, instance, *args, **kwargs):
    if 'post' in kwargs['action']:
        verifyExperts = VerifyExpert.objects.filter(project=instance)
        for verifyExpert in verifyExperts:
            verifyExpert.delete()

        for i in instance.categories.all():
            while True:
                if not VerifyExpert.objects.filter(project=instance, category=i).exists():
                    V = VerifyExpert(project=instance, category=i)
                    V.save()
                    if i.parent:
                        i = i.parent
                    else:
                        break


def EmployeeCountPreSave(sender, instance, *args, **kwargs):
    categories = instance.ve.project.categories
    a = instance.attrib

    for cat in categories.all():
        if a.parent == cat:
            return
    raise ValidationError('You cannot do this')


m2m_changed.connect(ProjectCategorym2m_change,
                    sender=Project.categories.through)
pre_save.connect(EmployeeCountPreSave, sender=EmployeeCount)
