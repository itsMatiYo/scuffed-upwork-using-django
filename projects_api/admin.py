from django.contrib import admin
from . import models

admin.site.register(models.VerifyExpert)
admin.site.register(models.Project)
admin.site.register(models.ProjectRequestEmployee)
admin.site.register(models.ProjectRequestVisitor)
admin.site.register(models.Parts)
admin.site.register(models.PayDateTime)
admin.site.register(models.EmployeeCount)
admin.site.register(models.Timer)
