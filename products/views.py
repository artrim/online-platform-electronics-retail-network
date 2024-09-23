from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from company.models import Company
from products.models import Product
from products.paginators import ProductPaginator
from products.serializers import ProductSerializer, ProductListSerializer, ProductDetailSerializer, \
    ProductUpdateSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPaginator

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action in ['list']:
            self.permission_classes = [IsAuthenticated]
            self.serializer_class = ProductListSerializer
        if self.action in ['retrieve']:
            self.permission_classes = [IsAuthenticated]
            self.serializer_class = ProductDetailSerializer
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
            self.serializer_class = ProductUpdateSerializer
        return super().get_permissions()

    def perform_create(self, serializer):
        product = serializer.save()
        company_customer = Company.objects.get(id=product.company.id)
        if company_customer.owner.id == self.request.user.id:
            product.save()
        else:
            product.delete()
            raise serializers.ValidationError('Вы не можете добавлять продукт в эту компанию')

    def perform_update(self, serializer):
        product = serializer.save()
        company_customer = Company.objects.get(id=product.company.id)
        if company_customer.owner.id == self.request.user.id:
            product.save()
        else:
            raise serializers.ValidationError('Вы не можете изменять продукт в этой компании')

    def perform_destroy(self, instance):
        company_customer = Company.objects.get(id=instance.company.id)
        if company_customer.owner.id == self.request.user.id:
            instance.delete()
        else:
            raise serializers.ValidationError('Вы не можете удалять продукт в этой компании')
