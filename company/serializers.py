from rest_framework import serializers

from company.models import Company, Supplier


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class CompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'name', 'email', 'country', 'city', 'street', 'number_home', 'owner')


class CompanyDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class CompanyUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = '__all__'


class SupplierUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('company_customer', 'company_supplier', 'debt')


class SupplierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('name_supplier', 'owner', 'id')
