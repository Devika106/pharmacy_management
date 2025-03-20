from django.db import models
from django.contrib.auth.models import User

# Medicine Model
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    batch_number = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    expiry_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.batch_number}"

# Billing Model
class Billing(models.Model):
    customer = models.CharField(max_length=100)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill for {self.customer} on {self.date}"
