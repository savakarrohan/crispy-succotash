from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
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
class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = "blog/post/list.html"
def post_share(request, post_id):
    """
    Form view to share by mail the post
    """
    post = get_object_or_404(Post, id = post_id, status=Post.status.PUBLISHED)
    sent = False
    if request.method == "POST":
        # When the form gets submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Send Email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url} \n \n {cd['name']} \'s comments {cd['name']}"
            send_mail(subject, message, 'rohansavakar@gmail.com', [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post, 'form':form, 'sent':sent})