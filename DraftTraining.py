from __future__ import unicode_literals

import numpy as np
from keras.models import Sequential, load_model
from keras.layers import GRU, LSTM, Dense, Dropout
from keras.utils import np_utils
from keras.optimizers import Adam
from keras.preprocessing.sequence import pad_sequences
import pickle
import os
from ArtificialImprovedDataset import ArtificialImprovedDatasetFactory
from Message import Message, LABELS
import BasicArtificialDataset

good_labels = [LABELS['Good'], LABELS['Discussion'], LABELS['Endorsed Automated']]

with open(os.getcwd() + '/messages.pkl', 'rb') as f:
    messages = pickle.load(f)

max_seq_len = 40
train_messages = 2500
test_messages = 2500
epochs = 1500
nodes = 64
nodes2 = 32
nodes3 = 32

# Basic artificial dataset
BasicArtificialDataset.make_fake_messages(train_messages + test_messages)
basic_artificial = BasicArtificialDataset.fake_messages


# Artificial improved dataset
def make_message_class(text, good):
    msg = Message(":0:abc:{0}".format(text))
    msg.label = LABELS['Discussion'] if good else LABELS['Repetitive']
    return msg

ArtificialImprovedDatasetFactory.NUM_MESSAGES = train_messages + test_messages
ads_factory = ArtificialImprovedDatasetFactory()
artificial_improved = map(lambda (msg, label): make_message_class(msg, label), zip(ads_factory.messages, ads_factory.labels))

# Real datset
real_dataset = [msg for msg in messages if msg.label != LABELS['Unknown']][:train_messages + test_messages]

# Reduced dataset
reduced_real = [msg for msg in real_dataset if msg.label in [LABELS['Repetitive'], LABELS['Discussion']]]

done = False
while not done:
    done = True
    ds_answer = raw_input('Use (r)eal dataset, re(d)uced real dataset, (b)asic artificial dataset, or artificial (i)mproved dataset?').lower()
    if ds_answer == 'r':
        messages = real_dataset
    elif ds_answer == 'd':
        messages = reduced_real
    elif ds_answer == 'b':
        messages = basic_artificial
    elif ds_answer == 'i':
        messages = artificial_improved
    else:
        done = False

for msg in messages:
    msg.make_ascii()
    msg.ignore_caps()

X = [([ord(c) for c in msg.message] + [-1.]) for msg in messages]
X = pad_sequences(X, maxlen=max_seq_len, dtype='float32')
X = np.reshape(X, (X.shape[0], max_seq_len, 1))
X /= np.linalg.norm(X)
y = np.array([(int(msg.label != LABELS['Repetitive'])) for msg in messages])

X_tr = X[:train_messages]
y_tr = y[:train_messages]
X_te = X[train_messages:train_messages + test_messages]
y_te = y[train_messages:train_messages + test_messages]

def begin_training():
    model = Sequential()
    model.add(GRU(nodes, batch_input_shape=(1, X_tr.shape[1], X_tr.shape[2]), stateful=True, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(GRU(nodes2, return_sequences=True, stateful=True))
    model.add(Dropout(0.1))
    model.add(GRU(nodes3, stateful=True))
    model.add(Dropout(0.1))
    model.add(Dense(1, activation='sigmoid'))

    # usually lr=0.0001
    model.compile(loss='binary_crossentropy', optimizer=Adam(lr=0.0001), metrics=['accuracy'])

    for i in xrange(epochs):
        run_epoch(model, X_tr, y_tr, i, i % 10 == 0, i % 100 == 0)

    evaluate(model, X_tr, y_tr, True)
    model.reset_states()

    model.save('model')
    return model


def run_epoch(model, Xe, ye, i, eval, save):
    model.fit(Xe, ye, nb_epoch=1, batch_size=1, verbose=1, shuffle=False)
    model.reset_states()
    print 'EPOCH {0}'.format(i)
    if eval:
        score_string_tr = evaluate(model, X_tr, y_tr, True)
        score_string_te = evaluate(model, X_te, y_te, False)
        with open(os.getcwd() + '/scores.txt'.format(i), 'a') as f:
            f.write(str(i) + " ")
            f.write(score_string_tr + " ")
            f.write(score_string_te)
            f.write('\n')
    if save:
        model.save('interim')


def load():
    return load_model('model')


def continue_training(model):
    for i in xrange(epochs):
        run_epoch(model, X_tr, y_tr, i, i % 10 == 0, i % 100 == 0)

    evaluate(model, X_tr, y_tr, True)
    model.reset_states()

    model.save('model')
    return model


def evaluate(model, X_eval, y_eval, training):
    print 'Training set begin' if training else 'Test set begin'
    model.reset_states()
    scores = model.evaluate(X_eval, y_eval, batch_size=1, verbose=0)
    model.reset_states()
    predicts = model.predict(X_eval[:100], batch_size=1)
    model.reset_states()
    for msg, predict in zip(messages[:100], predicts):
        print msg.message
        print predict
    print 'Training set end' if training else 'Test set end'
    score_string = "Model Accuracy: %.2f%%" % (scores[1]*100)
    print(score_string)
    return score_string

action = raw_input('Mode? (b)egin training, (c)ontinue training, or evaluate only').lower()
model = None
if action == 'b':
    model = begin_training()
else:
    model = load()

if action == 'c':
    continue_training(model)

evaluate(model, X_tr, y_tr, True)
evaluate(model, X_te, y_te, False)

with open(os.getcwd() + '/fake_set.pkl', 'wb') as f:
    pickle.dump(artificial_improved, f) 

