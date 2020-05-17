from keras import models
from gensim.models import word2vec
import jieba
import numpy as np
import jieba.posseg as pseg

jieba.load_userdict('F:\大创\抑郁症智能公益平台\\0项目\智能问答\简单的问题分类器\data\dict.txt')

def get_word2idx():
    f = open('F:\大创\抑郁症智能公益平台\\0项目\智能问答\简单的问题分类器\data\\word2idx.txt', 'r', encoding='utf-8')
    idx = f.read()
    f.close()
    idx = idx.split('\n')
    word2idx = {}
    for i in idx:
        word2idx[i.split(' ')[0].encode('utf-8').decode('utf-8-sig')] = int(i.split(' ')[1].encode('utf-8').decode('utf-8-sig'))
    return word2idx

word2idx = get_word2idx()

def to_vec(sequences, MAX_LENGTH = 10):
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

# def to_vec(sequences, MAX_LENGTH = 200):
#     results = np.zeros((len(sequences), MAX_LENGTH))
#     for i, sequence in enumerate(sequences):
#         for j in range(MAX_LENGTH):
#             if j < 4:
#                 results[i, 0] = 750.
#                 results[i, 1] = 171.
#                 results[i, 2] = 15495.
#                 results[i, 3] = 16955
#             else:
#                 results[i, j] = 0
#     return results


def predict(sentences):
    sentences = [jieba.lcut(sequence) for sequence in sentences]
    sentences = to_vec(sentences)
    print(sentences)
    model = models.load_model('first_dense_model.h5')
    return model.predict(sentences)


def get_name(sentence):
    words = pseg.cut(sentence)
    for w, t in words:
        if t == 'npg' or t == 'nb' or t == 'ng':
            return {w, t}
    return {'w': ''}

print(get_name('破译命运密码试一下'))