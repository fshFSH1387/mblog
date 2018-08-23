from django.conf.urls import url

# from blog.views import index
from blog.views import PostListView, PostDetailListView, PostdetailListView, ArchivesListView,CategoriesListView, \
    PostDetailView,TagsListView,search, index, searchindex,index,PostDetailViewPrime

app_name = 'blog'

urlpatterns = [
    # url(r'^index/$',index,name='index'),
    url(r'^index/$', PostListView.as_view(), name='index'),
    # url(r'^post_detail/(?P<pk>\d+)', PostDetailListView, name='post_detail'),
    # url(r'^detail/(?P<pk>\d+)/$', PostdetailListView.as_view(), name='detail'),
    # url(r'^post_detail/(?P<pk>\d+)/', PostDetailView.as_view(), name='post_detail'),
    url(r'^post_detail/(?P<pk>\d+)/', PostDetailViewPrime.as_view(), name='post_detail'),

    url(r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$', ArchivesListView.as_view(), name='archives'),
    url(r'^categories/(?P<pk>\d+)', CategoriesListView.as_view(), name='categories'),
    # url(r'^tags/(?P<pk>\d+)', TagsListView.as_view(), name='tags'),
    url(r'^tags/(?P<pk>\d+)', TagsListView.as_view(), name='tags'),
    # url(r'^tags/(?P<pk>\d+)', tags, name='tags'),
    # url(r'^search/$',search,name='search'),
    url(r'^search_index/$',index,name='search_index'),
    # url(r'^search_index/$',searchindex.as_view(),name='search_index'),

]
