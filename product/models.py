from django.db import models
from django.contrib.auth import get_user_model
from category.models import Category

User = get_user_model()


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='products')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    image = models.ImageField(upload_to='images')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
