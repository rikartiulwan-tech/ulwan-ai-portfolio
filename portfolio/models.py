
from django.db import models

class ClientInquiry(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    business_type = models.CharField(max_length=100)
    package = models.CharField(max_length=50)
    budget = models.CharField(max_length=50, default='$799')
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.business_type} - {self.package})"