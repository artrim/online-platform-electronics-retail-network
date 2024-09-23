from rest_framework import routers

from company.apps import CompanyConfig
from company.views import CompanyViewSet, SupplierViewSet

app_name = CompanyConfig.name

router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'supplier', SupplierViewSet, basename='supplier')

urlpatterns = [] + router.urls
