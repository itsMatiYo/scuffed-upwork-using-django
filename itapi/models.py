from django.db import models
from django.db.models.signals import pre_save

from projects_api.models import Project


class TimeTable(models.Model):
    DAY_CHOICES = [
        ('5', 'شنبه'),
        ('6', 'یک شنبه'),
        ('0', 'دو شنبه'),
        ('1', 'سه شنبه'),
        ('2', 'چهار شنبه'),
        ('3', 'پنج شنبه'),
        ('4', 'جمعه'),
    ]
    start = models.TimeField(max_length=24)
    end = models.TimeField(max_length=24)
    day = models.CharField(max_length=1, choices=DAY_CHOICES)

    class Meta:
        unique_together = ('start', 'end', 'day')


class TimeTableVisitor(models.Model):
    time = models.ForeignKey(TimeTable,
                             on_delete=models.PROTECT,
                             related_name='timetotable')
    visitor = models.ForeignKey("users.Visitor",
                                on_delete=models.PROTECT,
                                related_name='timetovisitor')
    date = models.DateField()
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name="timetoproject",
                                null=True, blank=True)

    class Meta:
        unique_together = ('time', 'visitor', 'date')


class Province(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(
        Province, on_delete=models.PROTECT, related_name='cities')
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'province']


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    parent = models.ForeignKey('self',
                               related_name='subcategories',
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)
    commission1 = models.PositiveSmallIntegerField(default=0)
    commission2 = models.PositiveSmallIntegerField(default=0)
    commission_employee1 = models.PositiveSmallIntegerField(default=0)
    commission_employee2 = models.PositiveSmallIntegerField(default=0)
    penalty = models.FloatField(null=True)

    def __str__(self):
        return self.title

    def get_level(self):
        par = self.parent
        level = 0
        while (par):
            level += 1
            par = par.parent
        return level

    @property
    def level(self):
        par = self.parent
        level = 0
        while (par):
            level += 1
            par = par.parent
        return level

    def get_top_category(self):
        par = self.parent
        while (par is not None):
            if par.parent is None:
                return par
            par = par.parent
        return self

    class Meta:
        ordering = ['parent__id']


class ReportEmployee(models.Model):
    rel_name = 'reportemps'
    project = models.ForeignKey('projects_api.Project',
                                on_delete=models.CASCADE,
                                related_name=rel_name)
    employee = models.ForeignKey('users.Employee',
                                 on_delete=models.PROTECT,
                                 related_name=rel_name)
    rep_expert = models.ForeignKey('users.Expert',
                                   on_delete=models.PROTECT,
                                   related_name=rel_name,
                                   blank=True,
                                   null=True
                                   )
    rep_customer = models.ForeignKey('users.Customer',
                                     on_delete=models.PROTECT,
                                     related_name=rel_name,
                                     blank=True,
                                     null=True
                                     )
    rep_cd = models.ForeignKey('users.CityAdmin',
                               on_delete=models.PROTECT,
                               related_name=rel_name,
                               blank=True,
                               null=True
                               )
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


def ReportEmployeePreSave(sender, instance, *args, **kwargs):
    if not instance.solve:
        instance.project.status = 'stopped'
    else:
        instance.project.status = 'doing'
    instance.project.save()


pre_save.connect(ReportEmployeePreSave, ReportEmployee)


class CompanyInfo(models.Model):
    id = models.PositiveSmallIntegerField(default=1,
                                          editable=False,
                                          primary_key=True)
    name = models.CharField(max_length=250)
    address = models.TextField()
    phonenums = models.JSONField(null=True)
    other = models.JSONField(null=True)
