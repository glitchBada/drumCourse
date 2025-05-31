from django.contrib import admin
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'short_content')
    

    def short_content(self, obj):
        return f"{obj.content[:100]}..." if len(obj.content) > 100 else obj.content
    short_content.short_description = 'Content Preview'

admin.site.register(BlogPost, BlogPostAdmin)