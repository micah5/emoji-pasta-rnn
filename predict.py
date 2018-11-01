__author__  = "Micah Price"
__email__   = "98mprice@gmail.com"

import config

from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils.data_utils import get_file
from keras.optimizers import RMSprop

import numpy as np
import random
import sys
import os
import io

def sample(a, temperature=1.0):
    # helper function to sample an index from a probability array
    a = np.log(a) / temperature
    dist = np.exp(a)/np.sum(np.exp(a))
    choices = range(len(a))
    return np.random.choice(choices, p=dist)

with io.open('data/selftexts.txt', encoding='utf-8') as f:
    text = f.read()

words = set(text.split())
words = sorted(words)

word_indices = dict((c, i) for i, c in enumerate(words))
indices_word = dict((i, c) for i, c in enumerate(words))

maxlen = 30
list_words=text.split()

model = load_model('models/selftexts.h5')

def generate_emoji_pasta(length):
    start_index = random.randint(0, len(list_words) - maxlen - 1)

    diversity = 1.5
    sentence = list_words[start_index: start_index + maxlen]
    generated = ' '.join(sentence)

    for i in range(length):
        x = np.zeros((1, maxlen, len(words)))
        for t, word in enumerate(sentence):
            x[0, t, word_indices[word]] = 1.
        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_word = indices_word[next_index]
        generated += next_word
        del sentence[0]
        sentence.append(next_word)
        sys.stdout.write(' ')
        if next_word == '<break>':
            sys.stdout.write('\n')
        else:
            sys.stdout.write(next_word)
        sys.stdout.flush()

generate_emoji_pasta(1000)
