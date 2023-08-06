import asyncio
import logging

import pyppeteer
import websockets
from pyppeteer.errors import TimeoutError
from scrapy.http import HtmlResponse

pyppeteer_level = logging.WARNING
logging.getLogger('websockets.protocol').setLevel(pyppeteer_level)
logging.getLogger('pyppeteer').setLevel(pyppeteer_level)


class PyppeteerMiddleware:
    def __init__(self, **args):
        """
        init logger, loop, browser
        :param args:
        """
        self.args = args
        self.loop = asyncio.get_event_loop()

    def __del__(self):
        """
        close loop
        :return:
        """
        self.loop.close()

    def render(self, url, retries=1, script=None, wait=0.3, scrolldown=False, sleep=0,
               timeout=8.0, keep_page=False):
        """
        render page with pyppeteer
        :param url: page url
        :param retries: max retry times
        :param script: js script to evaluate
        :param wait: number of seconds to wait before loading the page, preventing timeouts
        :param scrolldown: how many times to page down
        :param sleep: how many long to sleep after initial render
        :param timeout: the longest wait time, otherwise raise timeout error
        :param keep_page: keep page not to be closed, browser object needed
        :return: content, [result]
        """
        browser = self.loop.run_until_complete(pyppeteer.launch(headless=True,
                                                                handleSIGTERM=False,
                                                                handleSIGINT=False))

        # define async render
        async def async_render(inner_url, inner_script, inner_scrolldown, inner_sleep, inner_wait, inner_timeout,
                               inner_keep_page):
            try:
                # basic render
                page = await browser.newPage()
                await asyncio.sleep(inner_wait)
                response = await page.goto(inner_url, options={'timeout': int(inner_timeout * 1000)})
                if response.status != 200:
                    return None, None, response.status
                inner_result = None
                # evaluate with script
                if inner_script:
                    inner_result = await page.evaluate(inner_script)

                # scroll down for {scrolldown} times
                if inner_scrolldown:
                    for _ in range(inner_scrolldown):
                        await page._keyboard.down('PageDown')
                        await asyncio.sleep(inner_sleep)
                else:
                    await asyncio.sleep(inner_sleep)
                if inner_scrolldown:
                    await page._keyboard.up('PageDown')

                # get html of page
                page_content = await page.content()

                return page_content, inner_result, response.status
            except TimeoutError:
                return None, None, 500
            finally:
                # if keep page, do not close it
                if not inner_keep_page:
                    await page.close()

        content, result, status = [None] * 3

        # retry for {retries} times
        for i in range(retries):
            if not content:
                content, result, status = self.loop.run_until_complete(
                    async_render(inner_url=url, inner_script=script, inner_sleep=sleep, inner_wait=wait,
                                 inner_scrolldown=scrolldown, inner_timeout=timeout, inner_keep_page=keep_page))
            else:
                break
        self.loop.run_until_complete(browser.close())
        # if need to return js evaluation result
        return content, result, status

    def process_request(self, request, spider):
        """
        :param request: request object
        :param spider: spider object
        :return: HtmlResponse
        """
        if request.meta.get('render'):
            try:
                html, result, status = self.render(request.url, **self.args)
                return HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8',
                                    status=status)
            except websockets.exceptions.ConnectionClosed:
                pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(**crawler.settings.get('PYPPETEER_ARGS', {}))
