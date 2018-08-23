from django.db import models

# Create your models here.
#评论模型
'''
name
email
url
content
created_time
post
'''
class Comment(models.Model):
    name = models.CharField(max_length=64,verbose_name='名字')
    email = models.EmailField(verbose_name='邮箱')
    url = models.URLField(verbose_name='网址')
    context = models.TextField(verbose_name='评论')
    created_time = models.DateTimeField(auto_now_add=True)

    #所属博客，  外键
    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.context[:20]
