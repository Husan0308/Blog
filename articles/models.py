from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from accounts.models import UserRate

class Article(models.Model):
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=200, blank=True)
    body = RichTextField()
    photo = models.ImageField(upload_to='images/', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])
    
    @property
    def get_comments(self):
        return self.comments.filter(parent__isnull=True)
    
    @property
    def rates_count(self):
        count = self.rates.all().count()
        return count

 
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey("articles.Comment", on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    comment = models.CharField(max_length=150)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.comment
    
    def get_absolute_url(self):
        return reverse('article_list')
    
      
    @property
    def rates_count(self):
        count = self.rates.all().count()
        return count


    
