from django.db import models
from django.utils import timezone
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

# Create your models here.
class Idea(models.Model):
    objects = models.Manager()
    
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.title
        
class Comment(models.Model):
    
    author = models.ForeignKey('auth.User')
    idea = models.ForeignKey('idea.Idea', related_name="comments")
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.text