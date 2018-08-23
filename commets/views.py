from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import ListView

from blog.models import Post
from commets.forms import CommentModleForm
from commets.models import Comment


def post_comment(request,pk):
    post = get_object_or_404(Post,pk=pk)
    form = CommentModleForm()
    if request.method == 'POST':
        form = CommentModleForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = pk
            comment.save()
            # return redirect(reverse('blog:post_detail',kwargs={'pk':pk}))
        else:
            context = {
                'post':post,
                'form':form,
            }
            return render(request,'blog/detail.html',context)
    # return render(request,'blog/detail.html',{'form':form})
    return redirect(post)


#修改为通用类试图
class PostComment(CreateView):
    model = Comment
    template_name = 'blog/detail.html'
    fields = ['name','email','url','context']
    def get_success_url(self):
        return reverse('blog:post_detail',kwargs={'pk':self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(PostComment, self).get_context_data(**kwargs)
        post = get_object_or_404(Post,pk=self.kwargs['pk'])
        context.update({
            'post':post,
            'comment_list':post.comment_set.all()
        })
        # return super(PostComment, self).get_context_data()
        return context
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    def form_invalid(self, form):
        post = get_object_or_404(Post,self.kwargs['pk'])
        return render(self.request,'blog/detail.html',{
            'post':post,
            'comment_list':post.comment_set.all()
        })
