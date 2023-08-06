import time

from furl import furl
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider as BaseSpider, signals
from scrapy.spiders.crawl import Rule as BaseRule
from scrapy.utils.request import request_fingerprint
from scrapy_helper.core.fast_item import FastItem

from scrapy_helper.core.urls import get_domain
from scrapy_helper.core.utils import str2body, str2dict, str2list, convert_to_html, convert_to_text
from scrapy_helper.newspaper.article import Article


class Rule(BaseRule):
    def __init__(self, link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None,
                 process_request=None, errback=None,
                 method='GET', params=None, process_body=None, data=None, headers=None,
                 priority=0, dont_filter=False, cookies=None,
                 meta=None, dont_redirect=None, dont_retry=None,
                 handle_httpstatus_list=None, handle_httpstatus_all=None,
                 dont_cache=None, dont_obey_robotstxt=None,
                 download_timeout=None, max_retry_times=None, proxy=None, render=False, splash=None,
                 persist_filter=False, extract_article=False):
        super().__init__(link_extractor, callback, cb_kwargs, follow, process_links, process_request, errback)

        self.method = method
        self.params = str2dict(params)
        self.process_body = process_body
        self.data = str2body(data)
        self.headers = str2dict(headers)
        self.priority = priority
        self.dont_filter = dont_filter
        self.cookies = str2body(cookies)
        self.meta = str2dict(meta)
        self.dont_redirect = dont_redirect
        self.dont_retry = dont_retry
        self.handle_httpstatus_list = str2list(handle_httpstatus_list, lambda x: int(x))
        self.handle_httpstatus_all = handle_httpstatus_all
        self.dont_cache = dont_cache
        self.dont_obey_robotstxt = dont_obey_robotstxt
        self.download_timeout = download_timeout
        self.max_retry_times = max_retry_times
        self.proxy = proxy
        self.render = render
        self.splash = str2body(splash)
        self.persist_filter = persist_filter
        self.extract_article = extract_article

    def __str__(self):
        """
        object to str
        :return:
        """
        return str(self.__dict__.items())


class CrawlSpider(BaseSpider):
    name = None

    def start_requests(self):
        """
        override start requests
        :return:
        """
        self.crawler.signals.connect(self.make_start_requests, signal=signals.spider_idle)
        return []

    def make_start_requests(self):
        """
        make start requests
        :return:
        """
        for request in self.start():
            self.crawler.engine.slot.scheduler.enqueue_request(request)

    def start(self):
        """
        start requests
        :return:
        """
        for url in self.make_start_urls():
            yield Request(url)

    def make_start_urls(self):
        """
        get start urls
        :return:
        """
        return self.start_urls

    def _generate_request(self, rule_index, rule, link, response):
        """
        generate request by rule
        :param rule_index: rule index
        :param rule: rule object
        :param link: link object
        :return: new request object
        """
        url = furl(link.url).add(rule.params).url if rule.params else link.url

        # init request body
        body = None
        # process by method
        if rule.method.upper() == 'POST':
            # if process_body defined, use its result
            if callable(rule.process_body):
                body = rule.process_body(response)
            # if data defined in rule, use data
            if rule.data:
                body = rule.data

        meta = dict(**rule.meta)
        meta_items = ['dont_redirect', 'dont_retry', 'handle_httpstatus_list', 'handle_httpstatus_all',
                      'dont_cache', 'dont_obey_robotstxt', 'download_timeout', 'max_retry_times', 'proxy', 'render',
                      'splash', 'persist_filter', 'extract_article']
        meta_args = {meta_item: getattr(rule, meta_item) for meta_item in meta_items if
                     not getattr(rule, meta_item) is None}
        meta.update(**meta_args)
        meta.update(rule=rule_index, link_text=link.text)

        r = Request(
            url=url,
            method=rule.method,
            body=body,
            headers=rule.headers,
            cookies=rule.cookies,
            priority=rule.priority,
            dont_filter=rule.dont_filter,
            callback=self._callback,
            errback=self._errback,
            meta=meta,
        )

        return r

    @staticmethod
    def _get_request_fp(request):
        return request.meta.get('request_fp') or request_fingerprint(request)

    @staticmethod
    def convert_to_html(element):
        return convert_to_html(element)

    @staticmethod
    def convert_to_text(element):
        return convert_to_text(element)

    @staticmethod
    def join_to_html(texts):
        return convert_to_html(''.join(texts))

    @staticmethod
    def join_to_text(texts):
        return convert_to_text(''.join(texts))

    @staticmethod
    def fast_item(*args: str):
        _item = FastItem()
        _item.set(args)
        return _item

    def _callback(self, response):
        request_fp = self._get_request_fp(response.request)
        request_domain = get_domain(response.url)
        response.meta.update(request_fp=request_fp, request_domain=request_domain,
                             insert_time=time.strftime('%Y-%m-%d %H:%M:%S'))

        if response.meta['extract_article']:
            article = Article(url=response.url, html=response.body)
            article.parse()
            response.meta.update(
                article={"title": article.title, "text": article.text, "article_html": article.article_html,
                         "images": article.images, "movies": article.movies, "tags": article.tags,
                         "authors": article.authors, "top_img": article.top_img,
                         "meta_img": article.meta_img, "meta_keywords": article.meta_keywords,
                         "meta_description": article.meta_description, "meta_lang": article.meta_lang,
                         "publish_date": article.publish_date, "meta_favicon": article.meta_favicon,
                         "meta_site_name": article.meta_site_name, "meta_data": article.meta_data,
                         "canonical_link": article.canonical_link})

        rule = self._rules[response.meta['rule']]
        return self._parse_response(response, rule.callback, rule.cb_kwargs, rule.follow)

    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for rule_index, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            for link in rule.process_links(links):
                seen.add(link)
                # request = self._build_request(rule_index, link)
                request = self._generate_request(rule_index, rule, link, response)
                yield rule.process_request(request, response)
