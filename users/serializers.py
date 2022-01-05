from rest_framework.serializers import ModelSerializer
from itapi.models import TimeTable
from itapi.serializers import CategorySerializerReadOnly, CitySerializer
from users.models import CityAdmin, Commis, Employee, Expert, Resume, Visitor, Wallet


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class Resume_Serializer(ModelSerializer):
    class Meta:
        model = Resume
        fields = ('file',)


class Admin_Resume_Serializer(ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"
        read_only_fields = ('file',)


class CityAdminSerializer(ModelSerializer):
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = CityAdmin
        fields = '__all__'


class ExpertSerializer(ModelSerializer):
    class Meta:
        model = Expert
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializerReadOnly(read_only=True)
        self.fields['city'] = CitySerializer(read_only=True)
        self.fields['resume'] = Resume_Serializer(read_only=True)
        self.fields['employee'] = EmployeeSerializer(read_only=True)
        return super(ExpertSerializer, self).to_representation(instance)


class ExpertSerializerUpdate(ModelSerializer):
    class Meta:
        model = Expert
        exclude = ['employee', ]


class CommisSerializer(ModelSerializer):
    class Meta:
        model = Commis
        fields = '__all__'


class EmployeeSerializer(ModelSerializer):
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializerReadOnly(read_only=True)
        self.fields['resume'] = Resume_Serializer(read_only=True)
        return super(EmployeeSerializer, self).to_representation(instance)


class VisitorSerializer(ModelSerializer):
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = Visitor
        fields = '__all__'


# time_table serializer
class TimeTableSerializer(ModelSerializer):
    visitor = VisitorSerializer

    class Meta:
        model = TimeTable
        fields = '__all__'
