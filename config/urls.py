from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='users')),
    path('', include('company.urls', namespace='company')),
    path('', include('products.urls', namespace='products')),
]
