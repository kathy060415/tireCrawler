# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

# #다른 셀레니움
# from scrapy import signals
# from scrapy.http import HtmlResponse
# from scrapy.utils.python import to_bytes
#
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from time import sleep
#
# class ScrapyWithSeleniumSpiderMiddleware(object):
#
#
#     def from_crawler(cls, crawler):
#         print("this is ScrapyWithSeleniumSpiderMiddleware from_crawler ===================")
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
#
# class ScrapyWithSeleniumDownloaderMiddleware(object):
#
#
#     def from_crawler(cls, crawler):
#         print("this is ScrapyWithSeleniumSpiderMiddleware from_crawler +++++++++++++++++++++++")
#         middleware = cls()
#         crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
#         crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
#         return middleware
#
#     def spider_opened(self, spider):
#         CHROMEDRIVER_PATH = 'C:\Program Files (x86)\chromedriver.exe'
#         WINDOW_SIZE = "1920,1080"
#
#         chrome_options = Options()
#         # chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
#         chrome_options.add_argument("user-agent=Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
#
#         driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
#         self.driver = driver
#
#     def spider_closed(self, spider):
#         self.driver.close()
#
#     def process_request(self, request, spider):
#         self.driver.get(request.url)
#
#         # scrapy에서 셀레니움을 연동해서 사용할경우. 셀레니움의 동적인 크롤링 코드는 여기 미들웨어에서 작성해야 할것 같다.
#         # headless 옵션을 끄고 아래 결과가 동작하는지 보자. 동작을 확인했다.
#         bikeCompanyAllBtn = self.driver.find_element_by_xpath(
#             "#container > div.spot_main > div.spot_aside > div.tit > a")
#         bikeCompanyAllBtn.click()
#
#         body = to_bytes(text=self.driver.page_source)
#         sleep(5)
#         return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)
#
#
#     def process_response(self, request, response, spider):
#         return response
#
#     def process_exception(self, request, exception, spider):
#         pass

from time import sleep

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumMiddleware(object):

    @classmethod
    def from_crawler(cls, tireScrape):
        middleware = cls()
        tireScrape.signals.connect(middleware.spider_opened, signals.spider_opened)
        tireScrape.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        CHROMEDRIVER_PATH = 'C:\Program Files (x86)\chromedriver.exe'
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")

        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
        chrome_options.add_argument('lang=ko_KR')
        chrome_options.add_argument("user-agent=Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")

        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')

        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
        self.driver = driver

    def spider_closed(self, spider):
        self.driver.close()

    def process_request(self, request, spider):
        self.driver.get(request.url)

        body = to_bytes(text=self.driver.page_source)

        sleep(5)

        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)


class TirescrapeSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TirescrapeDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
