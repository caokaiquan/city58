# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..util.parse_old import parse,xiaoqu_parse,get_ershou_price_list,chuzu_list_pag_get_detail_url,get_chuzu_house_info
from ..items import Chuzu58Item,City58ItemXiaoChuZuQuInfo
from traceback import format_exc



class Spider58Spider(scrapy.Spider):
    name = 'spider_58'
    allowed_domains = ['58.com']
    host = 'gz.58.com'
    xiaoqu_url_format = 'http://{}/xiaoqu/{}/'
    xiaoqu_code = list()
    xiaoqu_code.append(1657)

    def start_requests(self):
        start_urls = ['http://{}/xiaoqu/{}/'.format(self.host,code) for code in self.xiaoqu_code]
        for url in start_urls:
            yield  Request(url)


    def parse(self, response):
        url_list = parse(response)
        for url in url_list:
            yield Request(url,callback= self.xiaoqu_detail_pag,errback=self.error_back)


    def xiaoqu_detail_pag(self,response):
        data = xiaoqu_parse(response)
        item = Chuzu58Item()
        item.update(data)
        item['id'] = response.url.split('/')[4]
        yield item

        # 二手房

        url = 'http://{}/xiaoqu/{}/ershoufang/'.format(self.host,item['id'])

        yield Request(url,callback= self.ershoufang_list_pag,meta={id:item['id']},errback= self.error_back)

        # 出租房
        url = 'http://{}/xiaoqu/{}/chuzu/'.format(self.host,item['id'])
        yield Request(url, callback=self.chuzu_list_pag, meta={id: item['id']}, errback=self.error_back)

    def ershoufang_list_pag(self, response):
        price_list = get_ershou_price_list(response)
        yield {id:response.meta['id'],price_list:price_list }

    def chuzu_list_pag(self, response):
        urls_list = chuzu_list_pag_get_detail_url(response)
        for url in urls_list:
            yield Request(url = url ,callback=self.chuzu_detail_pag,errback=self.error_back )

    def chuzu_detail_pag(self, response):
        data = get_chuzu_house_info(response)
        item = City58ItemXiaoChuZuQuInfo()
        item.update(data)
        item['id'] = response.meta['id']
        item['url'] = response.url
        yield item




    def error_back(self, e):
        _ = e
        self.logger.error(format_exc())