import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    """ Dynamically generate RSS or Atom feeds using site's framework
    """
    title = 'My blog'
    link = reverse_lazy('src.blog:post_list')
    description = 'New post'

    def items(self):
        """ Retrieves the objects to be included in the feed
        """
        return Post.published.all()[:5]

    def item_title(self, item):
        """ Return title of each object returned by items()
        """
        return item.title

    def item_description(self, item):
        """ Return description of each object returned by items()
        convert to HTML and cut after 30 words
        """
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        """ Return publication date of each object returned by items()
        """
        return item.publish
