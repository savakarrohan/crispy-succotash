from django.db import models
from django.utils import timezone

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
    # Publishing dates
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_=True)
    class Meta:
        """Ordering methodology metadata:"""
        ordering = ['-publish']
        indexes = [
            models.Index(fields=["-publish"]),
        ]
    
    def __str__(self) -> str:
        return self.title
    