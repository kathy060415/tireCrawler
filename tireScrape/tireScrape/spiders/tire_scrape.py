import scrapy
import pandas as pd
import parquet

class TireScrape(scrapy.Spider):
    name = 'tires'
    allowed_domains = ['tirerack.com']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'tireScrape.middlewares.SeleniumMiddleware': 100
        }
    }

    def start_requests(self):
        start_urls = [
            'https://www.tirerack.com/content/tirerack/desktop/en/tires/by-brand.html',
        ]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, method='GET', encoding='utf-8')

    def parse(self, response):
        for link in response.css('ul.clearfix a::attr(href)'):
            yield scrapy.Request(url="https://www.tirerack.com{}".format(link.get()),
                                   callback=self.parse_tire)

    def parse_tire(self, response):

        name = response.css('h1.brandNameHeader::text').extract()
        #quotes는 창 열 때마다 바뀐다는 점
        quotes = response.css('div.quote p::text').extract()
        tire_types = response.xpath('//*[@id="tr_tab_content_0"]/div/div/div/div/a/text()').extract()
        new_tires = response.xpath('//*[@id="tr_tab_content_1"]/div[2]/div/div/div/a/text()').extract()
        special_offers = response.xpath('//*[@id="tr_tab_content_3"]/div/h4/text()').extract()

        item = {
            'Name': name,
            'Quotes': quotes,
            'Tires': tire_types,
            'New Tires': new_tires,
            'Special Offers': special_offers
        }

        yield item

    # tire_df = pd.DataFrame(data=parse_tire.item)
    #
    # print(tire_df)

# # Selenium 연동 전에 작동 되는 코드
#작동이 되긴 하지만 리스트에 값이 반환 안됨
#     name = 'tires'
#     allowed_domains = ['tirerack.com']
#     custom_settings = {
#         'DOWNLOADER_MIDDLEWARES': {
#             'tireScrape.middlewares.SeleniumMiddleware': 100
#         }
#     }
#     # custom_settings = {
#     #     'DOWNLOADER_MIDDLEWARES': {
#     #         'tireScrape.middlewares.ScrapyWithSeleniumDownloaderMiddleware': 100
#     #     }
#     # }
#
#     start_urls = [
#         'https://www.tirerack.com/content/tirerack/desktop/en/tires/by-brand.html',
#     ]
#
#     def parse(self, response):
#         #list of hrefs (links to different brands)
#         for link in response.css('ul.clearfix a::attr(href)'):
#             # yield SplashRequest(url=("https://www.tirerack.com{}".format(link.get())),
#             #                     headers=self.headers, callback=self.parse_tire)
#             # yield response.follow(("https://www.tirerack.com{}".format(link.get())),
#             #                       headers=self.headers, callback=self.parse_tire)
#             yield response.follow(("https://www.tirerack.com{}".format(link.get())),
#                                   callback=self.parse_tire)
#             # yield response.follow(link.get(),
#             #               headers=self.headers, callback=self.parse_tire)
#             # yield response.follow(link.get(), callback=self.parse_tire)
#             # "https: // www.tirerack.com{}".format(response.css('ul.clearfix a::attr(href)').get())
#
#     def parse_tire(self, response):
#         # information = response.css('div.brand-info')
#
#         name = response.css('h1.brandNameHeader::text')
#         quotes = response.xpath('/html/body/div[4]/section/div/div/div/div/div/p/text()')
#         tire_types = response.xpath('//*[@id="tr_tab_content_0"]/div[2]/div[1]/div/div/a/text()')
#
#         yield {
#             'Name': name,
#             'Quotes': quotes,
#             'Tires': tire_types,
#
#         }
#         # for info in information:
#         #     yield{
#         #         'brand name': info.css('h1.brandNameHeader::text').get()
#         #     }

# Trial and Error-------------------------------------------------------------
    # # getting and following links of different brands
    # def parse(self, response):
    #     # print("hi")
    #     for link in response.xpath('//*[@id="ui-brandListBlog"]/div/ul/a/@href'):
    #         yield response.follow(link.get(), callback=self.parse_brand)
    #
    # def parse_brand(self, response):
    #     # print("Hi")
    #     information = response.xpath('//*[@id="brand-details"]/div')
    #     for info in information:
    #         yield{
    #             'name': info.xpath('//*[@id="brand-details"]/div/h1/text()').get()
    #         }

        # def parse(self, response):
    #     print('hi')
    #     for url in response.xpath('//*[@id="ui-brandListBlog"]/div/ul/a/@href').extract():
    #         yield scrapy.Request(response.urljoin("https://www.tirerack.com{}".format(url)
    #                                               , callback=self.parse_brandpage,
    #                                               dont_filter=True))
    #
    # def parse_brandpage(self, response):
    #     # brand_info = response.xpath('//*[@id="brand-details"]/div')
    #
    #     yield {
    #         'name': response.xpath('//*[@id="brand-details"]/div/h1/text()')
    #     }

# parse로 안넘어감
#     name = 'tires'
#     allowed_domains = ['www.tirerack.com']
#     i = 1
#     start_urls = [
#         'https://www.tirerack.com/content/tirerack/desktop/en/tires/by-brand.html',
#     ]
#
#     def parse(self, response):
#         print("hi")
#         for info in response.xpath('//*[@id="brand-details"]/div'):
#             yield{
#                 'brand name': info.xpath('h1/text()').extract_first()
#             }
#
#         next_page_url = response.xpath('/*[@id="ui-brandListBlog"]/div/ul/a[{}]'.format(self.i).get('href'))
#         print(next_page_url)
#         # next_page_url = ("https://www.tirerack.com{}"
#         #                  .format(response.xpath('//*[@id="ui-brandListBlog"]/div/ul/a[{}]'
#         #                                         .format(self.i))))
#         if next_page_url is not None:
#             yield scrapy.Request(response.urljoin("https://www.tirerack.com{}".format(next_page_url)))
#             print(next_page_url)
#
#         self.i += 1
