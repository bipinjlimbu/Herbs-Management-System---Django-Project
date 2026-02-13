from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        COLLECTOR = 'COLLECTOR', 'Collector'
        RETAILER = 'RETAILER', 'Retailer'

    role = models.CharField(max_length=15, choices=Role.choices, default=Role.COLLECTOR)
    phone = models.CharField(max_length=15, blank=True)

class CollectorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='collector_info')
    region = models.CharField(max_length=100, help_text="Area where they collect herbs")
    license_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Collector: {self.user.username}"

class RetailerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='retailer_info')
    shop_name = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return f"Retailer: {self.shop_name}"

class HerbBatch(models.Model):
    name = models.CharField(max_length=100)
    collector = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'COLLECTOR'})
    total_quantity = models.FloatField(help_text="In Kilograms")
    remaining_quantity = models.FloatField()
    harvest_date = models.DateField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.remaining_quantity}kg) - {self.collector.username}"

class RetailerInventory(models.Model):
    retailer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'RETAILER'})
    herb_name = models.CharField(max_length=100)
    current_stock = models.FloatField()
    original_batch = models.ForeignKey(HerbBatch, on_delete=models.SET_NULL, null=True)

class Transaction(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    collector = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    retailer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    batch = models.ForeignKey(HerbBatch, on_delete=models.CASCADE)
    quantity_bought = models.FloatField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)