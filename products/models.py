from django.db import models
from django.contrib.auth.models import User



# ---------------------------------
# CATEGORY
# ---------------------------------
class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = "Categories"



# ---------------------------------
# PRODUCT
# ---------------------------------
class Product(models.Model):

    # product owner
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(
        max_length=200
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # optional image
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    # optional description
    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.name} - {self.seller.username}"


    class Meta:
        ordering = ['-created_at']