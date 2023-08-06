from platinum2 import generate_user_agent
from scrapy import signals


class UserAgentMiddleware:
    def __init__(self, user_agent='Scrapy'):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        cls.mode = crawler.settings.get('USER_AGENT_MODE')
        cls.os = crawler.settings.get('USER_AGENT_OS')
        cls.navigator = crawler.settings.get('USER_AGENT_NAVIGATOR')
        cls.device_type = crawler.settings.get('USER_AGENT_DEVICE_TYPE')

        user_agent = generate_user_agent(os=cls.os, navigator=cls.navigator, device_type=cls.device_type)
        o = cls(user_agent)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent', self.user_agent)

    def process_request(self, request, spider):
        if self.mode == 'per':
            request.headers['User-Agent'] = generate_user_agent(os=self.os, navigator=self.navigator,
                                                                device_type=self.device_type)
        elif self.user_agent:
            request.headers.setdefault(b'User-Agent', self.user_agent)
