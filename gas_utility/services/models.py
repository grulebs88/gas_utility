from django.db import models
from django.contrib.auth.models import User

class ServiceRequest(models.Model):
    SERVICE_TYPE_CHOICES = (
        ('repair', 'Repair'),
        ('maintenance', 'Maintenance'),
        ('installation', 'Installation'),
    )
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    #customer = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')


    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_resolved = models.DateTimeField(null=True, blank=True)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)

    def __str__(self):
        return self.customer.username



