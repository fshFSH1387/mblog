import markdown
from django.contrib.sites import requests
from django.core.checks import Tags
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import resolve
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic import ListView
from django.utils.text import slugify
from django.views.generic.detail import SingleObjectMixin
from markdown.extensions.toc import TocExtension

from blog.models import Post, Tag, Category

# def index(request):
#     post_list=Post.objects.all()
#     return render(request,'blog/index.html',{'post_list':post_list})
from blog.utils import custom_paginator
from commets.forms import CommentModleForm


# def index(request):
#     post_list = Post.objects.all()
#     #对post_lsit进行分页
#     paginator = Paginator(post_list,3)
#     page = request.GET.get('page',None)
#     try:
#         posts = paginator.page(page)
#         pass
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     #返回野对象
#     return render(request,'blog/index.html',{'posts':posts})

# def index(request):
#     post_list = Post.objects.all()
#     # 对post_List进行分页
#     paginator = Paginator(post_list, 3)
#     # 从request中获取page
#     page = request.GET.get('page', None)
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # 给第一页
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     # 把页对象返回
#     # return render(request, 'blog/index.html', {'posts': posts, 'post_list': post_list})


class PostListView(ListView):
    model = Post
    # template_name_suffix = '_form'
    template_name = 'blog/index.html'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 从context中获取我们需要的数据
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        # 获取当前页page_obj.number
        start, end = custom_paginator(current_page=page_obj.number, num_pages=paginator.num_pages, max_page=5)
        context.update({
            'page_range': range(start, end + 1)
        })
        return context


def PostDetailListView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.content = markdown.markdown(post.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc'
    ])
    form = CommentModleForm()

    comment_list = post.comment_set.all()

    post.increase_views()

    return render(request, 'blog/detail.html', {'post': post, 'form': form, 'comment_list': comment_list})


# 将detail函数转换成通用类视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    # 重写get方法，以调用increase_view方法
    def get(self, request, *args, **kwargs):
        # 先调用父类的get方法
        response = super().get(request, *args, **kwargs)
        # 调用increase_view方法
        self.object.increase_views()
        # 最后别忘了返回response
        return response

    # 重写get_object方法，为了使用markdown渲染post的content
    def get_object(self, queryset=None):
        # 调用父类的get_object，以获取对象
        self.object = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify)
        ])
        self.object.content = md.convert(self.object.content)
        self.object.toc = md.toc
        # 返回object
        return self.object

    # 重写get_context_data方法，放入我们自己的上下文
    def get_context_data(self, **kwargs):
        # 调用父类的get_context_data方法，以获取当前context对象
        context = super().get_context_data(**kwargs)

        comment_list = self.object.comment_set.all()
        # 对post_List进行分页
        paginator = Paginator(comment_list, 1)
        # 从request中获取page
        page = self.request.GET.get('page', None)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            # 给第一页
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        start, end = custom_paginator(current_page=comments.number, num_pages=paginator.num_pages, max_page=5)
        context.update({
            'form': CommentModleForm(),
            'comments': comments,
            'page_range': range(start, end + 1),
        })
        # 返回context
        return context


# 优化PostDetailView
class PostDetailViewPrime(SingleObjectMixin, ListView):
    template_name = 'blog/detail.html'
    paginate_by = 1

    # 重写get方法
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # 调用increse_views
        self.object.increase_views()
        return super().get(request,*args, **kwargs)
        pass


    # 重写get_objext
    def get_object(self, queryset=Post.objects.all()):
        post = super().get_object(queryset=Post.objects.all())
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify)
        ])
        post.content = md.convert(post.content)
        post.toc = md.toc
        # 返回object
        return post
        pass

    # 重写get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 从context中获取我们需要的数据
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        start, end = custom_paginator(current_page=page_obj.number, num_pages=paginator.num_pages, max_page=5)
        context.update({
            'form': CommentModleForm(),
            'page_range': range(start, end + 1)
        })
        return context
    #重写get_querset
    def get_queryset(self):
        return self.object.comment_set.all()
#
#     pass
# class PostDetailViewPrime(SingleObjectMixin, ListView):
#     template_name = 'blog/detail.html'
#     paginate_by = 1
#
#     # 重写get方法
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         # 调用increase_views
#         self.object.increase_views()
#         return super().get(request, *args, **kwargs)
#
#     # 重写get_object
#     def get_object(self, queryset=Post.objects.all()):
#         post = super().get_object(queryset=Post.objects.all())
#         md = markdown.Markdown(extensions=[
#             'markdown.extensions.extra',
#             'markdown.extensions.codehilite',
#             TocExtension(slugify=slugify)
#         ])
#         post.content = md.convert(post.content)
#         post.toc = md.toc
#         # 返回object
#         return post
#
#     # 重写get_context_data方法
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # 从context中获取我们需要的数据
#         paginator = context.get('paginator')
#         page_obj = context.get('page_obj')
#         # 获取当前页page_obj.number
#         start, end = custom_paginator(current_page=page_obj.number, num_pages=paginator.num_pages, max_page=4)
#         context.update({
#             'form': CommentModleForm(),
#             'page_range': range(start, end + 1),
#         })
#         return context
#
#     # 重写get_queryset
#     def get_queryset(self):
#         return self.object.comment_set.all()




class PostdetailListView(DetailView):
    model = Post
    template_name_suffix = '_form'
    # context_object_name = 'post'
    # template_name = 'blog/post_form.html'


# 归档
class ArchivesListView(PostListView):
    def get_queryset(self):
        print((self.kwargs['month']))
        return super().get_queryset().filter(created_time__year=int(self.kwargs['year']),
                                             created_time__month=int(self.kwargs['month']))


# 分类
class CategoriesListView(PostListView):
    def get_queryset(self):
        return super().get_queryset().filter(category_id=self.kwargs['pk'])


# 标签云
class TagsListView(PostListView):
    # model = Tag
    # template_name = 'blog/index.html'
    # 传参数，需要用到的，，，
    def get_queryset(self):
        # print(tags()==self.kwargs['pk'])
        # taglist = Tag.objects.filter(id=self.kwargs['pk'])
        tag = get_object_or_404(Tag, id=self.kwargs['pk'])
        # taglists = Tag.objects.filter(xx=self.kwargs['pk'])

        return super().get_queryset().filter(tags=tag)


def search(request):
    q = request.GET.get('q', None)
    # 判断能不能获取到搜索关键字
    if q:
        # 进行搜索,根据q进行字段过滤
        object_list = Post.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(author__username__icontains=q))
        return render(request, 'blog/index.html', {'object_list': object_list})
        pass
    else:
        # 请输入
        msg = '请输入需要搜索的内容'
        return render(request, 'base.html', {'msg': msg})


def index(request):
    page = int(request.GET.get('page', None))
    if page:
        # 进行搜索,根据q进行字段过滤
        if page != None:
            return render(request, 'http://127.0.0.1:8000/blog/index/?page=%d' % (page))
            # return requests.RequestSite('http://127.0.0.1:8000/blog/index/?page=(%d)'%(qq))

        # object_list = Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(author__username__icontains=q))
        # return render(request,'blog/index.html',{'object_list':object_list})
        else:
            # 请输入
            return render(request, 'http://127.0.0.1:8000/blog/index/?page=%d' % (1))
        pass
    else:
        # 请输入
        msg = '请输入需要跳转的页数'
        return render(request, 'blog/index.html', {'msg': msg})
    pass


# class PostListView(ListView):
#     model = Post
#     # template_name_suffix = '_form'
#     template_name = 'blog/index.html'
#     paginate_by = 1
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # 从context中获取我们需要的数据
#         paginator = context.get('paginator')
#         page_obj = context.get('page_obj')
#         # 获取当前页page_obj.number
#         start, end = custom_paginator(current_page=page_obj.number, num_pages=paginator.num_pages, max_page=3)
#         context.update({
#             'page_range': range(start, end+1)
#         })
#         return context

class searchindex(PostListView):
    model = Post
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 从context中获取我们需要的数据
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        qq = context.get('qq')
        for item in range(paginator.num_pages):
            if qq == item:
                "?page={{ qq }}"
                pass
        return context

    pass
