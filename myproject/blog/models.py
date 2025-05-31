
from ckeditor.fields import RichTextField
from django.db import models

class BlogPost(models.Model):
    title = RichTextField(max_length=200)
    content = RichTextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title
    class Meta:

        verbose_name = "блог пост"
        verbose_name_plural = "Блог посты"
        ordering = ['-pub_date']