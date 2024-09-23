from django.db import models

from company.models import Company


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(max_length=255, verbose_name='название')
    product_models = models.CharField(max_length=100, verbose_name='модель')
    create_date = models.DateField(verbose_name='дата выхода продукта на рынок')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='компания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
