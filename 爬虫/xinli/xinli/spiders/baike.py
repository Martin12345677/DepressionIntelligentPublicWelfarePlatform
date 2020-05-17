# -*- coding: utf-8 -*-
import scrapy
from xinli.items import BookItem, PeopleItem, GainianItem
import json
import pymysql.cursors


class BaikeSpider(scrapy.Spider):
    name = 'baike'
    connect = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='depression',
        user='root',
        passwd='19981230',
        charset='utf8',
        use_unicode=True
    )
    cursor = connect.cursor()
#    allowed_domains = ['baidu.com']
#     start_urls = ['http://zy.zwbk.org/index.php/%E4%B8%AD%E6%96%87%E7%99%BE%E7%A7%91%E5%88%86%E7%B1%BB%E7%B4%A2%E5%BC%95_08_%E5%BF%83%E7%90%86%E7%A7%91%E5%AD%A6']
#     urls = ['https://www.psy525.cn/baike/list19.html', 'https://www.psy525.cn/baike/list15.html', 'https://www.psy525.cn/baike/list19.html']
#     items = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
#     s_urls = []
#     for u in urls:
#         for i in items:
#             s_urls.append(u[0: len(u)-5] + '/' + i + '.html')
#     start_urls = s_urls
#     url = 'https://jb.9939.com/jbzz/xinli/?page='
    url = 'http://jbk.39.net/bw/xinli_t1_p'
    s_urls = []
    for i in range(13):
        s_urls.append(url + str(i+1))
    start_urls = s_urls

    def parse(self, response):
        # print(response.css('table'))
        data = response.css('body').extract()
        print(data)
        for doc in data:
        #            with open('docs.txt', 'ab') as f:
        #                f.write((doc+'\n').encode())
            name = doc.css('::attr(title)').extract()
            url = doc.css('::attr(href)').extract()
            try:
                print(name, url, ' ok')
                # self.cursor.execute('update disease set group_ = %s where name = %s', (group, name))
                # self.cursor.execute('insert into disease(name, url) value (%s, %s)',(name, url))
            except:
                print(name+' failed')
                continue
            # doc = 'http://health.cq12320.cn/disease/detail?id=' + str(doc['DiseaseId'])
        #     self.cursor.execute('insert into disease(name, url) value (%s, %s)',(name, url))
        self.connect.commit()
        return
        #     try:
        #         yield scrapy.Request(doc, callback = lambda response, name=name : self.parse_doc(response, name))
        #     except:
        #         continue

    # clinical/symptom/treatment/prevention/group
    def parse_docs(self, response, url):
        table = response.css('table')[0]
        for doc in table.css('ul>li>a::attr(href)').extract():
            doc = 'http://zy.zwbk.org' + doc
            print(doc)
            try:
                yield scrapy.Request(doc, callback=lambda response, url=doc: self.parse_doc(response, url))
            except:
                continue
        
    def parse_doc1(self, response, url):
        open_type = ''
        name = response.css('#alllink_title::text').extract()[0]
        for t in response.css('.open_catgory::attr(value)').extract():
            open_type += t + ' '
        intro = ''
        for t in response.css('#custom_zy p::text').extract():
            intro += t + '\n'
        attrKey = response.css('.conBox>ul>li>span::text').extract()
        attrValue = response.css('.conBox>ul>li::text').extract()
        if '书' in open_type:
            item = BookItem()
        elif '人物' in open_type:
            item = PeopleItem()
        else:
            item = GainianItem()
        item['intro'] = intro
        item['opentype'] = open_type
        item['url'] = url
        item['name'] = name
        
#        with open('gainian.txt', 'ab') as f:
#            f.write(('  ' + intro + '\n').encode())
        for i in range(len(attrKey)):
            k = attrKey[i]
            if k == '作者：':
                k = 'author'
            elif k == '类别：':
                k = 'typeBook'
            elif k == '价格：':
                k = 'price'
            elif k == '语种：':
                k = 'language'
            elif k == 'ISBN：':
                k = 'ISBN'
            elif k == '出版社：':
                k = 'press'
            elif k == '出版时间：':
                k = 'time'
            elif k == '英文名：':
                k = 'englishName'
            elif k == '定义：':
                k = 'definition'
            elif k == '自然：':
                k = 'explanation'
            elif '扩展' in k:
                k = 'extend'
            elif k == '出处：' or k == '国籍：':
                k = 'from_'
            elif k == '出生地：':
                k = 'birthplace'
            elif k == '民族：':
                k = 'nation'
            elif k == '职业：':
                k = 'occupation'
            else:
                continue
            item[k] = attrValue[2 * i + 1][:len(attrValue[2 * i + 1])-5]
#            with open('gainian.txt', 'ab') as f:
#                f.write(('  ' + k + ':' + attrValue[2 * i + 1] + '\n').encode())
            
        return item


    def parse_doc(self, response, name):
        text = response.css('.disknow>div::text').extract()
        print(name)
        if text == [] or '资料完善中' in text[0] or '暂无相关资料' in text[0]:
            return
        else:
            content = ''
            for i in text:
                content += i
            # sql = ()
            # print(sql)
            self.cursor.execute('update disease set intro = %s where name = %s', (content, name))
            self.connect.commit()
            print(content)
            return
        #
        # try:
        #     name = ''
        #     p = response.css('div p')[0]
        #     p = p.css('::text')
        #     for i, pp in enumerate(p):
        #         intro += pp.extract()
        #         if i == 1:
        #             name = pp.extract()
        # except:
        #     print('err')
        #     return
