from haystack import indexes

from blog.models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    # 限制查询集
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
