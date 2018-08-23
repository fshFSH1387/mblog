from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# 扩展Uesr模型
class User(AbstractUser):
    # 昵称
    nickname = models.CharField(max_length=64, verbose_name='昵称')
    # 头像
    headshot = models.ImageField(upload_to='avatar/%Y/%m/%d', verbose_name='头像', default='defaule.jpg',null=True,blank=True)
    # 签名
    signature = models.CharField(max_length=128, default='这个家伙太懒了，什么都没留下来', verbose_name='个性签名',null=True,blank=True)

    class Meta(AbstractUser.Meta):
        pass
