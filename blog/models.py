from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    """ Post object """
    
    class Status(models.TextChoices):
        """ To chose between draft and published version of a post"""
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
        
    title = models.CharField(max_length=240)
    slug = models.SlugField(max_length=240)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # Publishing dates
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Choices for publishing
    status = models.CharField(max_length=2, choices=Status.choices, default= Status.DRAFT)
    class Meta:
        """Ordering methodology metadata:"""
        ordering = ['-publish']
        indexes = [
            models.Index(fields=["-publish"]),
        ]
    
    def __str__(self) -> str:
        return self.title
    