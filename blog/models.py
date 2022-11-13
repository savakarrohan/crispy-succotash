from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
class Post(models.Model):
    """ Post object """
    class Status(models.TextChoices):
        """ To chose between draft and published version of a post"""
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
    title = models.CharField(max_length=240)
    slug = models.SlugField(max_length=240, unique_for_date='publish')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # Publishing dates
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Choices for publishing
    status = models.CharField(max_length=2, choices=Status.choices, default= Status.DRAFT)
    
    objects = models.Manager()
    published = PublishedManager()
    class Meta:
        """Ordering methodology metadata:"""
        ordering = ['-publish']
        indexes = [
            models.Index(fields=["-publish"]),
        ]
    
    def __str__(self) -> str:
        return self.title
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year, self.publish.month, self.publish.day, self.slug] )
class Comment(models.Model):
    """
    Getting all the comments in to the database.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering=['created']
        indexes = [models.Index(fields=["created"])]
        
    def __str__(self):
        return f"Comment by {{self.name}} on {{self.post}}"