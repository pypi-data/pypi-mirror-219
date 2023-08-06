from tensorflow.keras.callbacks import LambdaCallback
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.utils import get_file
import numpy as np
import random
import sys
import io
import requests
import re
import logging
import os
from nltk.translate.bleu_score import corpus_bleu

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

r = requests.get("https://data.heatonresearch.com/data/t81-558/text/treasure_island.txt")
raw_text = r.text
print(raw_text[0:1000])

processed_text = raw_text.lower()
processed_text = re.sub(r'[^\x00-\x7f]', r'', processed_text)

print('corpus length:', len(processed_text))

chars = sorted(list(set(processed_text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(processed_text) - maxlen, step):
    sentences.append(processed_text[i: i + maxlen])
    next_chars.append(processed_text[i + maxlen])
print('nb sequences:', len(sentences))

print(sentences)

print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(chars))))
model.add(Dense(len(chars), activation='softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

model.summary()

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def on_epoch_end(epoch, _):
    # Function invoked at end of each epoch. Prints generated text.
    print("******************************************************")
    print('----- Generating text after Epoch: %d' % epoch)

    start_index = random.randint(0, len(processed_text) - maxlen - 1)
    for temperature in [0.2, 0.5, 1.0, 1.2]:
        print('----- temperature:', temperature)

        generated = ''
        sentence = processed_text[start_index: start_index + maxlen]
        generated += sentence
        print('----- Generating with seed: "' + sentence + '"')
        sys.stdout.write(generated)

        for i in range(400):
            x_pred = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, char_indices[char]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, temperature)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()

# Fit the model
print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

model.fit(x, y,
          batch_size=128,
          epochs=60,
          callbacks=[print_callback])

# Test veri setini hazırlama
test_sentences = []
test_next_chars = []
for i in range(0, len(processed_text) - maxlen, step):
    test_sentences.append(processed_text[i: i + maxlen])
    test_next_chars.append(processed_text[i + maxlen])
print('Test sequences:', len(test_sentences))

# Test veri setini vektörleştirme
x_test = np.zeros((len(test_sentences), maxlen, len(chars)), dtype=np.bool)
y_test = np.zeros((len(test_sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(test_sentences):
    for t, char in enumerate(sentence):
        x_test[i, t, char_indices[char]] = 1
    y_test[i, char_indices[test_next_chars[i]]] = 1

# Modelin tahminlerini almak
test_predictions = model.predict(x_test)

# Tahminleri sıkıştırma ve gerçek metinleri elde etme
test_predictions_compressed = [indices_char[np.argmax(prediction)] for prediction in test_predictions]
test_real_texts = [indices_char[np.argmax(label)] for label in y_test]

# BLEU skorunu hesaplama
bleu_score = corpus_bleu([[text] for text in test_real_texts], [test_predictions_compressed])

# BLEU skorunu yazdırma
print('BLEU score:', bleu_score)
