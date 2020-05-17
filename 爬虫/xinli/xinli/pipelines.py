# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors

class XinliPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                db='depression',
                user = 'root',
                passwd = '19981230',
                charset='utf8',
                use_unicode=True
                )
        self.cursor = self.connect.cursor();
        
        
    def process_item(self, item, spider):
        if('question' in item.keys()):
            f = open('F:\大创\抑郁症智能公益平台\\0项目\爬虫\\xinli\\gainian.txt', 'a', encoding='utf-8')
            f.write(item['question'] + '\n' + item['answer'] + '\n' + item['people'] + '\n')
            # self.cursor.execute(
            #         'insert into allquestion(question, answer, people, url) value (%s, %s, %s, %s)',
            #         (
            #                 item['question'],
            #                 item['answer'],
            #                 item['people'],
            #                 item['url']
            #                 )
            #         )

        else:
            if 'opentype' in item.keys():
                opentype = item['opentype']
            else:
                opentype = ''
                item['opentype'] = ''

            if '书' in opentype:
                for key in ['author', 'typeBook', 'price', 'language', 'ISBN', 'press', 'time', 'englishName']:
                    if key not in item.keys():
                        item[key] = ''
                # self.cursor.execute(
                #         'insert into book(name, url, intro, opentype, author, typeBook, price, language, ISBN, press, time, englishName) value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                #         (
                #                 item['name'],
                #                 item['url'],
                #                 item['intro'],
                #                 item['opentype'],
                #                 item['author'],
                #                 item['typeBook'],
                #                 item['price'],
                #                 item['language'],
                #                 item['ISBN'],
                #                 item['press'],
                #                 item['time'],
                #                 item['englishName']
                #                 )
                #         )
            elif '人物' in opentype:
                for key in ['from_', 'birthplace', 'nation', 'occupation', 'englishName']:
                    if key not in item.keys():
                        item[key] = ''
                # self.cursor.execute(
                #         'insert into people(name, url, intro, opentype, englishName, from_, birthplace, nation, occupation) value (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                #         (
                #                 item['name'],
                #                 item['url'],
                #                 item['intro'],
                #                 item['opentype'],
                #                 item['englishName'],
                #                 item['from_'],
                #                 item['birthplace'],
                #                 item['nation'],
                #                 item['occupation']
                #                 )
                #         )
            else:
                for key in ['definition', 'explanation', 'extend', 'englishName']:
                    if key not in item.keys():
                        item[key] = ''
                self.cursor.execute(
                        'insert into gainian(name, url, intro, opentype, englishName, definition, explanation, extend) value (%s, %s, %s, %s, %s, %s, %s, %s)',
                        (
                                item['name'],
                                item['url'],
                                item['intro'],
                                item['opentype'],
                                item['englishName'],
                                item['definition'],
                                item['explanation'],
                                item['extend']
                                )
                        )
                print('ok\n\n\n\n')
        self.connect.commit()
        return item
