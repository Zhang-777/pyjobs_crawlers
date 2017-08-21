# -*- coding: utf-8 -*-
import scrapy
from ..keywords import KWS
from ..items import PyjobItem
from ..pymods import xtract, xtract_list


class ItviecSpider(scrapy.Spider):
    name = "itviec"
    allowed_domains = ["itviec.com"]
    start_urls = [
        ("https://itviec.com/it-jobs/" + kw) for kw in KWS
    ]

    def parse(self, resp):
        if not resp.xpath('//div[@class="job__body"]'
                          '/*/a/@href').extract():
            for href in resp.xpath('//div[@class="job__body"]'
                                   '/*/*/a/@href').extract():
                if not href.startswith('/it-jobs/'):
                    continue
                yield scrapy.Request(resp.urljoin(href), self.parse_content)

    def parse_content(self, resp):
        item = PyjobItem()
        item['url'] = resp.url
        item['name'] = xtract(resp, ('//h1[@class="job_title"]/'
                                     'text()'))
        item["company"] = xtract(resp, ('//div[@class="employer-info"]/'
                                        'h3[@class="name"]/a/text()'))
        item["address"] = xtract(resp, ('//div[@class="address__full-address"]'
                                        '/span/text()'))
        item["expiry_date"] = ''
        item["post_date"] = ''
        item["province"] = xtract(resp, ('//div[@class="'
                                         'address__full-address"]'
                                         '/span[1]/'
                                         'text()'))

        jd = xtract(resp, ('//div[@class="job_description"]/'
                           'div[@class="description"]//text()'))
        item["work"] = jd

        item["specialize"] = xtract(resp, ('//div[@class="experience"]/'
                                           '/text()'))
        item["welfare"] = xtract(resp, ('//div[@class="culture_description"]/'
                                        'ul/li/text()'))
        item["wage"] = ''
        item["size"] = xtract(resp, ('//p[@class="group-icon"]/'
                                     'text()'))
        yield item
