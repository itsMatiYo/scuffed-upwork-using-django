from django.contrib import admin
from users import models


@admin.register(models.Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Employee)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Visitor)
class VisitorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CityAdmin)
class CityAdminAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Expert)
class CityAdminAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Resume)
class CityAdminAdmin(admin.ModelAdmin):
    pass
