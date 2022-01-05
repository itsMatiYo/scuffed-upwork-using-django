from django.core.exceptions import ValidationError
from users.serializers import ExpertSerializer
from . import models
from . import models
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from itapi.serializers import CategorySerializerReadOnly, ReportEmployeeSerializer4admin


class ProjectCreate(ModelSerializer):
    class Meta:
        model = models.Project
        fields = ['name', 'customer_deadline', 'customer_price', 'customer_description',
                  'file', 'categories', 'customer_price', 'need_visitor', ]

    def validate_categories(self, value):
        top_cat = value[0].get_top_category()
        for cat in value:
            for subcat in cat.subcategories.all():
                if subcat.subcategories.all().exists():
                    raise serializers.ValidationError(
                        'This is not a category for placing project in.')
            if cat.get_top_category() != top_cat:
                raise ValidationError(
                    'These categories are not for the same main category')
        return value

    def validate_city(self, value):
        if value:
            try:
                value.city_admin
                return value
            except:
                raise serializers.ValidationError(
                    'This City does not have admin')
        return value


class PartSerializer(ModelSerializer):
    class Meta:
        model = models.Parts
        fields = '__all__'


class ProjectUpdate4CustomerOwner(ModelSerializer):
    reportemps = ReportEmployeeSerializer4admin(read_only=True, many=True)

    class Meta:
        model = models.Project
        fields = ['name', 'customer_deadline', 'customer_description',
                  'file', 'categories', 'customer_price', 'reportemps', ]


class ProjectUpdate4TopExpert(ModelSerializer):
    reportemps = ReportEmployeeSerializer4admin(read_only=True, many=True)

    class Meta:
        model = models.Project
        fields = ['status', 'pre_price', 'experts_approve',
                  'price_expert', 'time_expert', 'description_expert', 'reportemps', ]


class ProjectRead(ModelSerializer):
    reportemps = ReportEmployeeSerializer4admin(read_only=True, many=True)

    class Meta:
        model = models.Project
        fields = '__all__'


class EmployeeCountSerializer(ModelSerializer):
    class Meta:
        model = models.EmployeeCount
        fields = '__all__'


class EmployeeCountSerializerUpdate(ModelSerializer):
    class Meta:
        model = models.EmployeeCount
        exclude = ['ve', ]

    def validate_attrib(self, value):
        if value.subcategories:
            return serializers.ValidationError({'category': 'is not attrib(last level)'})


class VerifyExpertSerializer(ModelSerializer):
    category = CategorySerializerReadOnly(read_only=True, required=False)
    empcounts = EmployeeCountSerializer(many=True, read_only=True)

    class Meta:
        model = models.VerifyExpert
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializerReadOnly(read_only=True)
        self.fields['expert'] = ExpertSerializer(read_only=True)
        return super(VerifyExpertSerializer, self).to_representation(instance)


class PayDateTimeSerializer(ModelSerializer):
    class Meta:
        model = models.PayDateTime
        fields = '__all__'
        read_only_fields = ['paid', ]


class PayDateTimeSerializerUpdate(ModelSerializer):
    class Meta:
        model = models.PayDateTime
        fields = '__all__'
        read_only_fields = ('paid', 'project',)


class ProjectRead4CustomerOwner(ModelSerializer):
    reportemps = ReportEmployeeSerializer4admin(read_only=True, many=True)
    verifies = VerifyExpertSerializer(many=True, read_only=True)

    class Meta:
        model = models.Project
        fields = '__all__'
