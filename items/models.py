from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):

    CATEGORY_CHOICES = [
        ('Phone', 'Phone'),
        ('Laptop', 'Laptop'),
        ('ID Card', 'ID Card'),
        ('Wallet', 'Wallet'),
        ('Bag', 'Bag'),
        ('Keys', 'Keys'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Lost', 'Lost'),
        ('Found', 'Found'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    item_name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    location = models.CharField(max_length=100)
    date = models.DateField()

    image = models.ImageField(
        upload_to='items/',
        blank=True,
        null=True
    )

    contact = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name