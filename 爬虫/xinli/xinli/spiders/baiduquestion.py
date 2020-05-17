# -*- coding: utf-8 -*-
import scrapy
from xinli.items import BaiduquestionItem


class BaiduquestionSpider(scrapy.Spider):
    name = 'baiduquestion'
    # allowed_domains = ['baikemy.com']
    start_urls = ['https://www.baikemy.com/search/disease/list?searchType=ARTICLE&pageIndex=1&pageSize=150&keyWord=%E6%8A%91%E9%83%81%E7%97%87']

    def parse(self, response):
        for a in response.css('.answer-list::attr(href)').extract():
            a = 'https://www.baikemy.com' + a
            try:
                yield scrapy.Request( a , callback = lambda response, url = a: self.parse_a(response, url))
            except:
                continue

    def parse_a(self, response, url):
        print('ok')
        question = response.css('.detail_name span::text').extract()[0]
        people = ''
        answer = ''
        for p in response.css('.right_item_expert_info span::text').extract():
            people += p + ' '
        for a in response.css('.content::text').extract():
            answer += a + '\n'
        item = BaiduquestionItem()
        item['url'] = url
        item['question'] = question
        item['people'] = people
        item['answer'] = answer
        return item