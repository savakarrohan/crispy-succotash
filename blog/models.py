from django.db import models

# Create your models here.
class Post(models.Model):
    """ Post object """
    title = models.CharField(max_length=240)
    slug = models.SlugField(max_length=240)
    body = models.TextField()
    
    def __str__(self) -> str:
        return self.title
    