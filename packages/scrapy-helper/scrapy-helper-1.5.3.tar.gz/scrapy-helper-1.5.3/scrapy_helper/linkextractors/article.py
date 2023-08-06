from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from scrapy_helper.core.urls import valid_news_url


class ArticleLinkExtractor(LxmlLinkExtractor):
    pass

    def _link_allowed(self, link):
        allowed = super()._link_allowed(link)
        if allowed:
            return valid_news_url(link.url)

        return allowed
