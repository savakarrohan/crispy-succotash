from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(counts=5):
    latest_posts = Post.published
    return {
        "request": request,
    }
