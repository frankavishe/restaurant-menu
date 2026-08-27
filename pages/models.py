from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    contact_info = models.CharField(max_length=254)
    message = models.TextField(max_length=2000)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} ({self.submitted_at:%Y-%m-%d %H:%M})"
