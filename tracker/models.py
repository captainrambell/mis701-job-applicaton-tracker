from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    url = models.URLField()
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title} at {self.company}"


class Application(models.Model):
    STATUS_TO_APPLY = "To Apply"
    STATUS_APPLIED = "Applied"
    STATUS_INTERVIEW = "Interview"
    STATUS_OFFER = "Offer"
    STATUS_REJECTED = "Rejected"

    STATUS_CHOICES = [
        (STATUS_TO_APPLY, "To Apply"),
        (STATUS_APPLIED, "Applied"),
        (STATUS_INTERVIEW, "Interview"),
        (STATUS_OFFER, "Offer"),
        (STATUS_REJECTED, "Rejected"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    applied_date = models.DateField(null=True, blank=True)
    next_step_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.job.title} - {self.status}"


class Contact(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name} ({self.role})"
