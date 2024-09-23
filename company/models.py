from django.db import models

from users.models import User

SUPPLIERS_TYPE = [('individual', 'индивидуальный'), ('factory', 'завод'), ('retail', 'розничный')]
NULLABLE = {'blank': True, 'null': True}


class Company(models.Model):
    """Модель компании."""
    name = models.CharField(unique=True, max_length=255, verbose_name='название')
    email = models.EmailField(unique=True, verbose_name='почта')
    country = models.CharField(max_length=50, verbose_name='страна')
    city = models.CharField(max_length=50, verbose_name='город')
    street = models.CharField(max_length=50, verbose_name='улица')
    number_home = models.CharField(max_length=50, verbose_name='номер дома')
    level_company = models.IntegerField(default=0, verbose_name='уровень компании')
    type_company = models.CharField(max_length=30, choices=SUPPLIERS_TYPE, verbose_name='тип компании')
    supplier_name = models.CharField(max_length=100, verbose_name='имя компании', **NULLABLE)
    supplier_id = models.IntegerField(verbose_name='id компании поставщика', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец компании', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'компания'
        verbose_name_plural = 'компании'


class Supplier(models.Model):
    """Модель поставщика"""
    name_supplier = models.CharField(max_length=100, verbose_name='имя компании-поставщика', **NULLABLE)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='задолженность')
    create_time = models.DateTimeField(verbose_name='время создания', auto_now_add=True)
    company_customer = models.IntegerField(verbose_name='компания-заказчик')
    company_supplier = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='компания-поставщик')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return self.name_supplier

    class Meta:
        verbose_name = 'поставщик'
        verbose_name_plural = 'поставщики'
