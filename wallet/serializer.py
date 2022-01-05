from rest_framework import serializers


class EditOptionSerializer(serializers.Serializer):
    name = serializers.CharField()
    min_deposit = serializers.IntegerField()
    max_deposit = serializers.IntegerField()
    min_withdrawal = serializers.IntegerField()
    max_withdrawal = serializers.IntegerField()
    max_capacity = serializers.IntegerField()


class NameSerializer(serializers.Serializer):
    name = serializers.CharField()


class PaymentSerializer(serializers.Serializer):
    amount = serializers.CharField()
    wallet_id = serializers.CharField()


class FilterSerializer(serializers.Serializer):
    filter = serializers.DictField(required=False)
    sort_by = serializers.CharField(required=False)
    sort_type = serializers.IntegerField(required=False)
    per_page = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False)


class Part_Create_Serializer(serializers.Serializer):
    service_id = serializers.CharField()
    wallet_id = serializers.CharField()
    name = serializers.CharField()
    amount = serializers.IntegerField()


class Part_Spend_Serializer_Helper_Section(serializers.Serializer):
    wallet_id = serializers.CharField()
    percent = serializers.IntegerField()


class Spend_Type_one_Serializer(serializers.Serializer):
    amount = serializers.IntegerField()
    service_id = serializers.CharField()
    description = serializers.CharField()
    sections = Part_Spend_Serializer_Helper_Section(many=True)


class Withdrawal_Create_Serializer(serializers.Serializer):
    service_id = serializers.CharField()
    wallet_id = serializers.CharField()
    amount = serializers.IntegerField()


class Withdrawal_UJ_Serializer(serializers.Serializer):
    tracking_code = serializers.CharField(required=False)
    description = serializers.CharField(required=False)


class Description_Serializer(serializers.Serializer):
    description = serializers.CharField()


class Card_Serializer(serializers.Serializer):
    service_id = serializers.CharField()
    amount = serializers.IntegerField()
    expire_at = serializers.DateField(
        input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'])
    wallet_ids = serializers.ListSerializer(
        child=serializers.CharField())


class Spend_Type_Two_Serializer(serializers.Serializer):
    wallet_id = serializers.CharField()
    amount = serializers.IntegerField()
    service_id = serializers.CharField()
    description = serializers.CharField()
    password = serializers.CharField(required=False)
    sections = Part_Spend_Serializer_Helper_Section(many=True)


class Gitcard_Serializer(serializers.Serializer):
    service_id = serializers.CharField()
    amount = serializers.IntegerField()
    expire_at = serializers.DateField(
        input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'])


class Filter_Transaction_Serializer(serializers.Serializer):
    filter = serializers.DictField(required=False)
    sort_by = serializers.CharField(required=False)
    sort_type = serializers.IntegerField(required=False)
    per_page = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False)
    from_date = serializers.DateField(
        input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'], required=False)
    to_date = serializers.DateField(
        input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'], required=False)
