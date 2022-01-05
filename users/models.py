from django.db import models


class Resume(models.Model):
    file = models.FileField()
    STATUS_CHOICES = [
        ('ns', 'noot_seen'),
        ('np', 'not_approved'),
        ('ap', 'approved')
    ]
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=3,
                              default='ns')
    reason = models.TextField(blank=True)


class Wallet(models.Model):
    id = models.CharField(max_length=40, primary_key=True)

    def __str__(self):
        return self.id


class Employee(models.Model):
    yellow_cards = models.PositiveIntegerField(default=0)
    approved = models.BooleanField(default=False)
    wallet = models.OneToOneField("Wallet",
                                  on_delete=models.CASCADE,
                                  related_name='employee')
    city = models.ForeignKey('itapi.City',
                             related_name='employee',
                             on_delete=models.PROTECT,
                             null=True)
    resume = models.OneToOneField(Resume,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  related_name='employee')
    category = models.ForeignKey('itapi.Category',
                                 on_delete=models.SET_NULL,
                                 related_name='employees',
                                 null=True)


def __str__(self):
    return self.wallet.pk


class Visitor(models.Model):
    # yellow_cards = models.PositiveIntegerField(default=0)
    city = models.ForeignKey('itapi.City',
                             related_name='visitor',
                             on_delete=models.PROTECT,
                             null=True)
    wallet = models.OneToOneField("Wallet",
                                  on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    resume = models.OneToOneField(Resume,
                                  on_delete=models.SET_NULL,
                                  related_name='visitor',
                                  null=True,
                                  blank=True)

    def __str__(self):
        return self.wallet.pk


class Customer(models.Model):
    city = models.ForeignKey('itapi.City',
                             related_name='customer',
                             on_delete=models.PROTECT,
                             null=True)
    wallet = models.OneToOneField("Wallet",
                                  on_delete=models.CASCADE)

    def __str__(self):
        return self.wallet.pk


class CityAdmin(models.Model):
    city = models.OneToOneField('itapi.City',
                                related_name='city_admin',
                                on_delete=models.PROTECT,
                                null=True)
    wallet = models.OneToOneField("Wallet",
                                  on_delete=models.CASCADE)

    def __str__(self):
        return self.wallet.pk


class Expert(models.Model):
    yellow_cards = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('itapi.Category',
                                 on_delete=models.SET_NULL,
                                 related_name='experts',
                                 null=True)
    # ! Expert's city is employee's city
    employee = models.OneToOneField(Employee,
                                    on_delete=models.CASCADE,
                                    related_name='expert',
                                    null=True)

    def is_it_top(self):
        return not(self.category.parent)

    def __str__(self):
        return self.employee.wallet.pk


class Commis(models.Model):
    id = models.PositiveSmallIntegerField(default=1,
                                          editable=False,
                                          primary_key=True)
    visitor = models.PositiveSmallIntegerField()
    cityadmin = models.PositiveSmallIntegerField()
