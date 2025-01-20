from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField('user.CustomUser', related_name='like_posts')
    author = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return