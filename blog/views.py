from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
def post_detail(request, year, month, day, post):
    """Detail view for each post"""
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    # Comments
    # List the comments in the respective post
    comments = post.comments.filter(active=True)
    # Form for the users to comment
    form = CommentForm

    # Implementing the tags information
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "publish"
    )[:4]
    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
    )

    # Post_List view shouldn't have been deleted


def post_list(request, tag_slug=None):
    """
    Post list view which is a functional view
    """
    # Create the initial query set
    post_list = Post.published.all()
    tag = None
    # If a tag_slug exists query set of all respective tags only.
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If the page is not an integer
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        "blog/post/list.html",
        {
            "posts": posts,
            "tag": tag,
        },
    )


class PostListView(ListView):
    """
    Alternative post list view
    """

    queryset = Post.published.all()
    context_object_name = "posts"
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
            message = f"Read {post.title} at {post_url} \n \n {cd['name']} 's comments {cd['name']}"
            send_mail(subject, message, "rohansavakar@gmail.com", [cd["to"]])
            sent = True
        else:
            form1 = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form1, "sent": sent}
    )


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
    return render(
        request,
        "blog/post/comment.html",
        {
            "post": post,
            "form": form,
            "comment": comment,
        },
    )
