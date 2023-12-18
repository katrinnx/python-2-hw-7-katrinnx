import scrapy
from urllib.parse import urlencode
from spider_steam.items import SpiderSteamItem
import re

queries = ['adventure', 'dragons', 'expedition']  # запросы
API = ''


def get_url(url):
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class SteampSpider(scrapy.Spider):
    name = 'SteamSpider'
    allowed_domains = ['store.steampowered.com']

    def start_requests(self):
        for query in queries:
            for i in range(1, 3):
                url = 'https://store.steampowered.com/search/?' + urlencode({'term': query, 'page': i})
                yield scrapy.Request(url=url, callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        products = set()
        for res in response.css('a[class = "search_result_row ds_collapse_flag "]::attr(href)').extract():
            if 'agecheck' not in res:
                products.add(res)
        for product in products:
            yield scrapy.Request(url=product, callback=self.parse_product_page)

    def parse_product_page(self, response):
        items = SpiderSteamItem()
        name = response.xpath('//div[@id="appHubAppName"][@class="apphub_AppName"]/text()').extract()
        category = response.xpath('//div[@class="blockbg"]/a/text()').extract()
        num_of_reviews = response.xpath('//div[@itemprop="aggregateRating"]/div[@class="summary column"]/span[@class="responsive_hidden"]/text()').extract()
        total_grade = response.xpath('//div[@itemprop="aggregateRating"]/div[@class="summary column"]/span[@class="game_review_summary positive"]/text()').extract()
        release_date = response.xpath('//div[@class="release_date"]/div[@class="date"]/text()').extract()
        developer = response.xpath('//div[@class="dev_row"]/div[@id="developers_list"]/a/text()').extract()
        tags = response.xpath('//div[@class="glance_tags popular_tags"]/a/text()').extract()
        price = response.xpath('//div[@class="game_purchase_price price"]/text()')[0].extract()
        available_platforms = response.xpath('//div[@class="sysreq_tabs"]/div/text()').extract()

        items['name'] = ''.join(name).strip().replace('™', '')
        items['category'] = '/'.join(map(lambda x: x.strip(), category[1:])).strip()
        items['num_of_reviews'] = ''.join(re.sub(r'\D', '', str(num_of_reviews))).strip()
        items['total_grade'] = ''.join(total_grade).strip()
        items['release_date'] = ''.join(release_date).strip()
        items['developer'] = ', '.join(map(lambda x: x.strip(), developer)).strip()
        items['tags'] = ', '.join(map(lambda x: x.strip(), tags)).strip()
        items['price'] = ''.join(price).strip().replace('уб', '')
        items['available_platforms'] = ', '.join(map(lambda x: x.strip(), available_platforms)).strip()

        year = '2000'
        if len(items['release_date']) > 0:
            year = items['release_date'].split()[-1]
        if year >= '2000' and name != '':
            yield items
