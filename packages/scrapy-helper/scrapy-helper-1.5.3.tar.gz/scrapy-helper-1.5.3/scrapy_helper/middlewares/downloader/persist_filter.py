import redis
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.request import request_fingerprint


class PersistFilterMiddleware:
    def __init__(self):
        self.client: redis.Redis = None
        self.__redis_pool: redis.ConnectionPool = None

    @classmethod
    def from_crawler(cls, crawler):
        cls.redis_host = crawler.settings.get('PERSIST_FILTER_REDIS_HOST')
        cls.redis_port = crawler.settings.get('PERSIST_FILTER_REDIS_PORT')
        cls.redis_password = crawler.settings.get('PERSIST_FILTER_REDIS_PASSWORD')
        cls.persist_filter_name = crawler.settings.get('PERSIST_FILTER_NAME')

        o = cls()
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        self.__redis_pool = redis.ConnectionPool(
            host=self.redis_host, port=self.redis_port, password=self.redis_password, decode_responses=True)
        self.client = redis.Redis(connection_pool=self.__redis_pool)

    def spider_closed(self, spider):
        self.__redis_pool.disconnect()

    @staticmethod
    def _get_request_fp(request):
        fp = request_fingerprint(request)
        request.meta['request_fp'] = fp
        return fp

    def process_request(self, request, spider):
        fp = self._get_request_fp(request)
        if request.meta.get('persist_filter'):
            key_name = self.persist_filter_name or spider.name
            fp_exists = self.client.sismember(key_name, fp)
            if fp_exists:
                raise IgnoreRequest("Skipping URL. Already scrapped or in pipeline.")
            else:
                self.client.sadd(key_name, fp)
                return None
