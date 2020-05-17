# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json
from keras import models
import jieba
import jieba.posseg as pseg
import numpy as np
from py2neo import Graph
import datetime
from ..models import History
import os


def get_word2idx():
    f = open(os.path.join(os.path.dirname(__file__), 'word2idx.txt'), 'r', encoding='utf-8')
    idx = f.read()
    f.close()
    idx = idx.split('\n')
    word2idx = {}
    for i in idx:
        word2idx[i.split(' ')[0].encode('utf-8').decode('utf-8-sig')] = int(i.split(' ')[1].encode('utf-8').decode('utf-8-sig'))
    return word2idx


def to_vec(sequences, MAX_LENGTH = 10):
    word2idx = get_word2idx()
    results = np.zeros((len(sequences), MAX_LENGTH))
    for i, sequence in enumerate(sequences):
        for j in range(MAX_LENGTH):
            if j < len(sequence):
                word = sequence[j].encode('utf-8').decode('utf-8-sig')
                try:
                    results[i, j] = word2idx[word]
                except:
                    results[i, j] = 0
            else:
                results[i, j] = 0
    return results


def predict(sentences):
    sentences = [jieba.lcut(sequence) for sequence in sentences]
    sentences = to_vec(sentences)
    model = models.load_model(os.path.join(os.path.dirname(__file__), 'first_dense_model.h5'))
    return model.predict(sentences)


def get_name(sentence):
    words = pseg.cut(sentence)
    for w, t in words:
        if t == 'npe' or t == 'nb' or t == 'ng':
            return {'w': w, 't': t}
    return {'w': ''}


def make_reply(type, detail):
    print(detail)
    graph = Graph('http://localhost:7474', username='neo4j', password='neo4j')
    if 't' not in detail.keys():
        # 缺库处理
        return {
            'reply': '这个我还不太知道。'
        }
    t = detail['t']
    name = detail['w']
    label = ''
    if t == 'npe':
        label = 'people'
    elif t == 'ng':
        label = 'gainian'
    elif t == 'nb':
        label = 'book'
        name = '《' + name + '》'
    else:
        #缺库处理
        return {
            'reply': '这个我还不太知道。'
        }
    node = graph.find_one(label, 'name', name)
    print(node, label, name)
    if type == 0:
        return {'reply': node['intro']}
    elif type == 1:
        opentype = node['opentype']
        opentype = opentype[:len(opentype) - 1].replace(' ', '、')
        return {'reply': opentype}
    elif type == 2:
        return {'reply': name + '来自' + node['from_']}
    elif type == 4:
        return {'reply': name + '：' + node['author']}
    elif type == 3:
        occupation = node['occupation']
        occupation = occupation[:len(occupation) - 2].replace(' ', '、')
        return {'reply': name + '的职业是' + occupation}
    elif type == 5:
        return {'reply': node['price']}
    elif type == 6:
        return {'reply': node['language']}
    elif type == 7:
        return {'reply': name + '的ISBN是' + node['ISBN']}
    elif type == 8:
        return {'reply': node['press']}
    elif type == 9:
        return {'reply': '访问' + node['url'] + '可查看' + name + '的详细信息'}


def reply(request):
    jieba.load_userdict(os.path.join(os.path.dirname(__file__), 'dict.txt'))
    if request.method == 'POST':
        try:
            sentence = request.POST['sentence']
        except:
            sentence = request.GET['sentence']
        email = request.POST.get('email', '')
        receive_time = request.POST.get('time', '')
        history = History(email=email, text=sentence, time=receive_time, send=True)
        history.save()
        type = np.argmax(predict([sentence])[0])
        detail = get_name(sentence)
        rep = make_reply(type, detail)
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        history = History(email=email, text=rep['reply'], time=time, send=False)
        history.save()
        msg = {
            'text': rep['reply'],
            'time': time,
            'send': False
        }
        rep = {
            'msg': msg
        }
        return HttpResponse(json.dumps(rep))


    # return HttpResponse(json.dumps(get_name('破译命运密码试一下')))
