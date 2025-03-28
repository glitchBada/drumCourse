from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title