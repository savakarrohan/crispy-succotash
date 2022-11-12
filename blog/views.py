from django.shortcuts import render
from .models import Post
from django.http import Http404
# Create your views here.
def post_list(request):
    """ Post list view"""
    posts = Post.published.all()
    return render(request,'blog/post/list.html',{'posts':posts})
def post_detail(request, id):
    """Detail view for each post"""
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    
    return render(request,'blog/post/detail.html',{
        'post':post
    })