from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from company.models import Company, Supplier
from company.paginators import CompanyPaginator, SuppliersPaginator
from company.permissions import IsCompanyOwner, IsSupplierOwner

from company.serializers import CompanySerializer, CompanyDetailSerializer, CompanyListSerializer, \
    CompanyUpdateSerializer, SupplierSerializer, SupplierListSerializer, SupplierUpdateSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = CompanyPaginator
    filter_backends = (filters.SearchFilter,)
    search_fields = ('country',)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
            self.serializer_class = CompanySerializer
        if self.action in ['list']:
            self.permission_classes = [AllowAny]
            self.serializer_class = CompanyListSerializer
        if self.action in ['retrieve']:
            self.permission_classes = [IsAuthenticated, IsCompanyOwner]
            self.serializer_class = CompanyDetailSerializer
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsCompanyOwner]
            self.serializer_class = CompanyUpdateSerializer
        return super().get_permissions()

    def perform_create(self, serializer):
        company = serializer.save()
        company.owner = self.request.user
        company.save()
        return company


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    pagination_class = SuppliersPaginator

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated]
            self.serializer_class = SupplierListSerializer
        if self.action in ['retrieve']:
            self.permission_classes = [IsAuthenticated, IsSupplierOwner]
            self.serializer_class = SupplierSerializer
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsSupplierOwner]
            self.serializer_class = SupplierUpdateSerializer
        return super().get_permissions()

    def perform_create(self, serializer):
        supplier = serializer.save()
        company_customer = Company.objects.get(id=supplier.company_customer)
        supplier.owner = self.request.user
        supplier.save()

        if company_customer.type_company == 'individual' or company_customer.type_company == 'retail':
            Company.objects.filter(id=company_customer.id).update(
                level_company=2, supplier_name=supplier.company_supplier.name,
                supplier_id=supplier.company_supplier.id,
            )
            supplier.name_supplier = company_customer.name
            supplier.owner = self.request.user
            supplier.save()
        elif company_customer.type_company == 'factory':
            supplier.name_supplier = company_customer.name
            supplier.save()
            Company.objects.filter(id=company_customer.id).update(
                level_company=1, supplier_name=supplier.company_supplier.name,
                supplier_id=supplier.company_supplier.id
            )
        return supplier

    def perform_update(self, serializer):
        supplier = serializer.save()
        company_customer = Company.objects.get(id=supplier.company_customer)

        if company_customer.type_company == 'individual' or company_customer.type_company == 'retail':
            supplier.name_supplier = company_customer.name
            supplier.owner = self.request.user
            supplier.save()
            Company.objects.filter(id=company_customer.id).update(
                level_company=2, supplier_name=supplier.company_supplier.name,
                supplier_id=supplier.company_supplier.id,
            )
        elif company_customer.type_company == 'factory':
            supplier.name_supplier = company_customer.name
            supplier.owner = self.request.user
            supplier.save()
            Company.objects.filter(id=company_customer.id).update(
                level_company=1, supplier_name=supplier.company_supplier.name,
                supplier_id=supplier.company_supplier.id
            )
        return supplier
