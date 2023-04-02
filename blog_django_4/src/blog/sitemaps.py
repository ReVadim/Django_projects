from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    """ Sitemap framework to generate sitemap of website
    """
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        """ returns the QuerySet of objects to include in sitemap
        """
        return Post.published.all()

    def lastmod(self, obj):
        """ returns the last time the object was modified
        """
        return obj.updated
