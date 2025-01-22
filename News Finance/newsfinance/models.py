from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class NewsSource(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class NewsCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "News Categories"

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    content = models.TextField()
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    source_url = models.URLField()
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "News"

class FinancialIndicator(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    current_value = models.DecimalField(max_digits=20, decimal_places=2)
    change_value = models.DecimalField(max_digits=20, decimal_places=2)
    change_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField()
    source = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class APILog(models.Model):
    endpoint = models.CharField(max_length=200)
    request_data = models.JSONField(null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)
    status_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.endpoint} - {self.timestamp}"
