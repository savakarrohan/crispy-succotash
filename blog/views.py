from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
# Create your views here.
def post_list(request):
    """ Post list view"""
    post_list = Post.published.all()
    # Paginator with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer
        posts = paginator.page(1)
    except EmptyPage:
        # IF page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'posts':posts})
def post_detail(request, year, month, day, post):
    """Detail view for each post"""
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
    
    return render(request,'blog/post/detail.html',{
        'post':post
    })