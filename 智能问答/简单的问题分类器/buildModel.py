import jieba.posseg as pseg
import jieba, os, re
from gensim.models import word2vec
import numpy as np
from keras.layers import Embedding, Dense, Flatten, LSTM
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras import models

jieba.load_userdict('F:\大创\抑郁症智能公益平台\\0项目\智能问答\简单的问题分类器\data\dict.txt')

path = 'F:\大创\抑郁症智能公益平台\\0项目\智能问答\简单的问题分类器\data'
f = open(os.path.join(path, 'train_data.txt'), 'r', encoding='utf-8')
train_data = f.read()
f.close()
f = open(os.path.join(path, 'test_data.txt'), 'r', encoding='utf-8')
# f = open(os.path.join(path, 'val_data.txt'), 'r', encoding='utf-8')
test_data = f.read()
f.close()

# sourse = open('F:\大创\抑郁症智能公益平台\\0项目\爬虫\\xinli\\gainian.txt', 'r', encoding='utf-8').read()
#
# sourse = re.sub(r'[\r\na-z]', '', sourse)
#
# words = jieba.cut(sourse)
#
# f = open(os.path.join(path, 'words.txt'), 'a', encoding='utf-8')
#
# for word in words:
#     if word not in [' ', '~', '`', '"', '?', '/', '	', '「', '」', '(', ')', '：', '——', '？', '-', '“', '”', '……', '。', '，', '：', '；', '？', '！', ':', '.', '!', '《', '》','\'', '（', '）', '…', '￥', '[', ']', '、', ',']:
#         f.write(word + ' ')
# f.close()


#预训练word2vec
# sentences = word2vec.Text8Corpus(os.path.join(path, 'words.txt'))
#
# model = word2vec.Word2Vec(sentences, sg=1, size=100, hs=100, min_count=1, window=3)
#
# model.save('word2vec.bin')


embedding_model = word2vec.Word2Vec.load('word2vec.bin')

word2idx = {}
_word2idx = {0: 'null'}

f = open(os.path.join(path, 'word2idx.txt'), 'w', encoding='utf-8')

vocab_list = [(k, embedding_model.wv[k]) for k, v in embedding_model.wv.vocab.items()]

embeddings_matrix = np.zeros((len(embedding_model.wv.vocab.items()) + 1, embedding_model.vector_size))

for i in range(len(vocab_list)):
    word = vocab_list[i][0]
    word2idx[word] = i + 1
    _word2idx[i + 1] = word
    if i != 0:
        f.write('\n' + word + ' ' + str(i + 1))
    else:
        f.write(word + ' ' + str(i + 1))
    embeddings_matrix[i + 1] = vocab_list[i][1]

train_sentences = [sentence.split(' ')[0] for sentence in train_data.split('\n')]
train_labels = [int(sentence.split(' ')[1].encode('utf-8').decode('utf-8-sig')) for sentence in train_data.split('\n')]
test_sentences = [sentence.split(' ')[0] for sentence in test_data.split('\n')]
test_labels = [int(sentence.split(' ')[1].encode('utf-8').decode('utf-8-sig')) for sentence in test_data.split('\n')]


#打乱数据
indices = np.random.choice(len(train_sentences), len(train_sentences), replace=False)
train_sentences = np.array(train_sentences)[indices]
train_labels = np.array(train_labels)[indices]
indices = np.random.choice(len(test_sentences), len(test_sentences), replace=False)
test_sentences = np.array(test_sentences)[indices]
test_labels = np.array(test_labels)[indices]

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

train_words = [jieba.lcut(s) for s in train_sentences]
test_words = [jieba.lcut(s) for s in test_sentences]

MAX_LENGTH = 10

def to_vec(sequences):
    results = np.zeros((len(sequences), MAX_LENGTH))
    for i, sequence in enumerate(sequences):
        sen = []
        for j in range(MAX_LENGTH):
            if j < len(sequence):
                word = sequence[j].encode('utf-8').decode('utf-8-sig')
                try:
                    sen.append(word2idx[word])
                except:
                    sen.append(0)
            else:
                sen.append(0)
        results[i] = sen
    return results

train_x = to_vec(train_words)
test_x = to_vec(test_words)

val_num = 1000
val_x = test_x[:val_num]
val_labels = test_labels[:val_num]
test_x = test_x[val_num:]
test_labels = test_labels[val_num:]

model = Sequential()
model.add(Embedding(29043, 100, input_length=MAX_LENGTH))
model.add(Flatten())
# model.add(Dense(64, activation='relu', input_shape=(MAX_LENGTH,)))
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))
model.layers[0].set_weights([embeddings_matrix])
model.layers[0].trainable = False

model.summary()

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_x,
                    train_labels,
                    epochs=21,
                    batch_size=512,
                    validation_data=(test_x, test_labels))

model.save('first_dense_model.h5')

print(model.evaluate(val_x, val_labels))
def to_text(sequences):
    texts = []
    for sequence in sequences:
        text = ''
        for w in sequence:
            text += _word2idx[int(w)]
        texts.append(text)
    return texts

# results = model.predict(val_x)
# texts = to_text(val_x)
# for i, r in enumerate(results):
#     print(texts[i], np.argmax(r))
