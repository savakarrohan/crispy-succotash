import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostFeed(Feed):
    titel = "My Blog"
    link = reverse_lazy("blog:post_list")
    description = "new posts from my blog."

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item) -> str:
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item) -> str:
        return item.publish
