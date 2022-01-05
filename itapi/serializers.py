from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from . import models


class CategorySerializer4Admin(ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

    def validate_commission2(self, value):
        if value >= 0 and value < 50:
            return value
        else:
            raise serializers.ValidationError(
                'commission1 not between 0 and 50')

    def validate_commission1(self, value):
        if value >= 0 and value < 50:
            return value
        else:
            raise serializers.ValidationError(
                'commission1 not between 0 and 50')


class CategorySerializer4AdminUpdate(CategorySerializer4Admin):
    class Meta:
        model = models.Category
        fields = '__all__'
        read_only_fields = ['parent', ]

    def validate_commission2(self, value):
        if value >= 0 and value < 50:
            return value
        else:
            raise serializers.ValidationError(
                'commission1 not between 0 and 50')

    def validate_commission1(self, value):
        if value >= 0 and value < 50:
            return value
        else:
            raise serializers.ValidationError(
                'commission1 not between 0 and 50')


class CategorySerializerReadOnly(ModelSerializer):
    class Meta:
        model = models.Category
        exclude = ('commission1', 'commission2',
                   'commission_employee1', 'commission_employee2')


class CitySerializer(ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'


class ProvinceSerializer(ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = models.Province
        fields = '__all__'


# time_table serializer
class TimeTableSerializer(ModelSerializer):
    class Meta:
        model = models.TimeTable
        fields = '__all__'

    def validate(self, attrs):
        start = attrs.get('start')
        end = attrs.get('end')
        if start < end:
            return super().validate(attrs)
        else:
            raise serializers.ValidationError(
                'start time and end time do not match.')


# report_employee serializer


class ReportEmployeeSerializer4admin(ModelSerializer):
    class Meta:
        model = models.ReportEmployee
        fields = '__all__'
        extra_kwargs = {'rep_expert': {'required': False},
                        'rep_customer': {'required': False},
                        'rep_cd': {'required': False}}


class TimeTableVisitorSerializerCreate(ModelSerializer):
    class Meta:
        model = models.TimeTableVisitor
        exclude = ('project', 'visitor',)
        # extra_kwargs = {
        #     'visitor': {'required': False}
        # }

        # def save(self) -> None:
        # if self.date.weekday() != int(self.time.day):
        #     raise ValidationError('date not match with this time table day')
        # return super().save()

    def validate(self, attrs):
        my_date = attrs.get('date')
        my_time = attrs.get('time')
        if my_date.weekday() == int(my_time.day):
            return super().validate(attrs)
        else:
            raise serializers.ValidationError(
                'Date day and time day are not same')


class TimeTableVisitorSerializerUpdate4Customer(ModelSerializer):
    class Meta:
        model = models.TimeTableVisitor
        fields = ['project', ]


class TimeTableVisitorSerializer(ModelSerializer):
    class Meta:
        model = models.TimeTableVisitor
        fields = '__all__'


class CompanyInfoSerializer(ModelSerializer):
    class Meta:
        model = models.CompanyInfo
        fields = '__all__'
