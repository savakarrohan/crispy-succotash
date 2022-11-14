from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
# Create your views here.
def post_detail(request, year, month, day, post):
    """Detail view for each post"""
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
    # Comments
    # List the comments in the respective post
    comments = post.comments.filter(active=True)
    # Form for the users to comment
    form = CommentForm
    return render(request,'blog/post/detail.html',{
        'post':post,
        'comments':comments,
        'form':form,
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
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    form1 = EmailPostForm()
    if request.method == "POST":
        # When the form gets submitted
        form1 = EmailPostForm(request.POST)
        if form1.is_valid():
            cd = form1.cleaned_data
            # Send Email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url} \n \n {cd['name']} \'s comments {cd['name']}"
            send_mail(subject, message, 'rohansavakar@gmail.com', [cd['to']])
            sent = True
        else:
            form1 = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form1, 'sent':sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # What happens when a comment is published.
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a comment object without saving to database
        comment = form.save(commit=False)
        # Assign post to comment
        comment.post = post
        # Save the comment to database
        comment.save()
    return render(request, 'blog/post/comment.html',{'post':post, 'form': form, 'comment':comment,})