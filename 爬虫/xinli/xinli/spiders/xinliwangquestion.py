# -*- coding: utf-8 -*-
import scrapy
from xinli.items import BaiduquestionItem


class XinliwangquestionSpider(scrapy.Spider):
    name = 'xinliwangquestion'
    # allowed_domains = ['baikemy.com']
    url = 'http://www.psy.com.cn/xinlihuzhu/search.asp?act=2&page='
    start_urls = []
    for i in range(80):
        start_urls.append(url + str(i+1))
    def parse(self, response):
        for a in response.css('#main table td a::attr(href)').extract():
            a = 'http://www.psy.com.cn/xinlihuzhu/' + a
            try:
                yield scrapy.Request( a , callback = lambda response, url = a: self.parse_a(response, url))
            except:
               continue

    def parse_a(self, response, url):
        print('ok')
        question = response.css('#left-main>div>div::text').extract()[2]
        question += response.css('b::text').extract()[0]
        people = ''
        answer = ''
        isAnswer = False
        for a in response.css('#left-main>div>div::text').extract():
            if '最佳答案' in a:
                isAnswer = True
            elif '其他回答' in a or '\t\r\n' in a:
                isAnswer = False
            elif isAnswer:
                answer += a + '\n'
        item = BaiduquestionItem()
        item['url'] = url
        item['question'] = question
        item['people'] = people
        item['answer'] = answer
        return item