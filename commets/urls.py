from django.conf.urls import url

# from blog.views import index
from blog.views import PostListView, PostDetailListView, PostdetailListView, ArchivesListView,CategoriesListView
from commets.views import post_comment,PostComment

app_name = 'comments'

urlpatterns = [
        # url(r'comments/(?P<pk>\d+)/$',post_comment,name='post_comment'),
        url(r'comments/(?P<pk>\d+)/$',PostComment.as_view(),name='post_comment'),
]
