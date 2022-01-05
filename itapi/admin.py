from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.City)
admin.site.register(models.Province)
admin.site.register(models.TimeTable)
admin.site.register(models.TimeTableVisitor)
admin.site.register(models.ReportEmployee)
