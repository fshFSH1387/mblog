from django.contrib.syndication.views import Feed
from .models import Post


#定义rss订阅feed
class ALLPostFeed(Feed):
    #title表示我们的feed在集合阅读器上显示的标题
    title = 'python行天下'

    #link表示要跳转的链接
    link = '/blog/index'

    #描述信息
    description = 'python新点get'


    #需要显示的条目
    def items(self):
        return Post.objects.all()

    #集合器中显示的内容条目的标题
    def item_title(self,item):
        return '[%s]%s'%(item.category,item.title)

    #聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.content


