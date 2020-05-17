#coding:utf-8
from py2neo import Graph, Node
import os
import numpy as np
import re
import jieba
from gensim.models import word2vec

graph = Graph('http://localhost:7474', username='neo4j', password='neo4j')

labels = ['gainian', 'people', 'book']
names = []
path = 'F:\大创\抑郁症智能公益平台\\0项目\智能问答\简单的问题分类器\data'

# f = open(os.path.join(path, 'dict.txt'), 'a', encoding='utf-8')
text = ''
for label in labels:
    nodes = graph.find(label=label)
    for node in nodes:
        if not node['intro']:
            continue
        # name = node['name']
        intro = node['intro']
        text += intro + '\n'
        # if 'http' in name or len(name) > 100:
        #     continue
        # name = re.sub("[《》]+", "", name)
        # names.append(name)
#         if label == 'gainian':
#             f.write(name + ' 2000 ng\n')
#         elif label == 'book':
#             f.write(name + ' 2000 nb\n')
#         else:
#             f.write(name + ' 2000 npe\n')
# f.close()


#制作词向量
sourse = re.sub(r'[\r\na-z]', '', text)

words = jieba.cut(sourse)

f = open(os.path.join(path, 'words.txt'), 'a', encoding='utf-8')

for word in words:
    if word not in [' ', '~', '`', '"', '?', '/', '	', '「', '」', '(', ')', '：', '——', '？', '-', '“', '”', '……', '。', '，', '：', '；', '？', '！', ':', '.', '!', '《', '》','\'', '（', '）', '…', '￥', '[', ']', '、', ',']:
        f.write(word + ' ')
f.close()


#预训练word2vec
sentences = word2vec.Text8Corpus(os.path.join(path, 'words.txt'))

model = word2vec.Word2Vec(sentences, sg=1, size=100, hs=100, min_count=1, window=3)

model.save('word2vec.bin')



def get_random_names():
    ns = []
    for i in np.random.choice(len(names), 100):
        ns.append(names[i])
    return ns




def make_data(type, question1='', question2=''):
    ns = get_random_names()
    f = open(os.path.join(path, 'train_data.txt'), 'a', encoding='utf-8')
    for n in ns:
        question = question1 + n + question2
        f.write(question + ' ' + str(type) + '\n')
        print(question)
    f.close()

# f = open(os.path.join(path, '问题模板.txt'), 'r', encoding='utf-8')
# questions = f.read().split('\n')
# for q in questions:
#     q = q.split(' ')
#     type = q[0]
#     q = q[1].split('*')
#     question1 = q[0]
#     question2 = q[1]
#     make_data(type, question1, question2)
