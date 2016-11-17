from __future__ import unicode_literals

import numpy as np
from keras.models import Sequential, load_model
from keras.layers import GRU, LSTM, Dense, Dropout
from keras.utils import np_utils
from keras.optimizers import Adam
from keras.preprocessing.sequence import pad_sequences
import pickle, random, os
from operator import add
from GenerateArtificialDataset import ArtificialDatasetFactory

LABELS = {
    'Unknown':              (-1),
    'Bad':                  (-2),
    'Good':                 (-3),
    'Discussion':           0,
    'Endorsed Automated':   1,
    'Repetitive':           2,
    'Offensive':            3,
    'Link':                 4,
    'Non-English':          5,
    }

good_labels = [LABELS['Good'], LABELS['Discussion'], LABELS['Endorsed Automated']]

class Message:     
    def __init__(self, raw_string):
        parts = raw_string.split(':')

        if len(parts) < 4:
            if 'PING' in raw_string:
                error = 'PING message'
            elif 'DECODE ERROR' in raw_string:
                error = 'Unicode error in message'
            else:
                error = 'Invalid message format'
            raise ValueError(error)     

        self.timestamp = int(parts[1].strip(': '))
        self.username = parts[2].split('!')[0].strip(':! ')
        self.message = reduce(add, parts[3:]).strip('\n')
        self.label = LABELS['Unknown']
        

        
def make_ascii(msg):
    msg.message = msg.message.encode('ascii', 'ignore')

def ignore_caps(msg):
    msg.message = msg.message.lower()
        
with open(os.getcwd() + '/messages.pkl', 'rb') as f:
    messages = pickle.load(f)

fake_messages = []
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'x', 'z']    
repetitive_phrases = {'kappa': 0, 'pogchamp': 0, 'ghost': 0, 'git': 0, 'lul': 0, 'wutface': 0, 'damn son': 0}

def make_fake_messages(num):
    global fake_messages
    
    def make_message(text, good):
        global fake_messages
        msg = Message(":0:abc:{0}".format(text))
        msg.label = LABELS['Good'] if good else LABELS['Bad']
        fake_messages += [msg]

    def gen_random_text():
        global fake_messages
        text = str()
        for pos in xrange(random.randint(1, 30)):
            text += alphabet[random.randint(0, 25)]
        return text

    for i in xrange(num): 
        if random.randint(0, 1) == 1:
            phrase = repetitive_phrases.keys()[random.randint(0, len(repetitive_phrases) - 1)]
            make_message(phrase, repetitive_phrases[phrase] == 0)
            repetitive_phrases[phrase] = 30
        else:
            make_message(gen_random_text(), True)
        for phrase in repetitive_phrases.keys():
            repetitive_phrases[phrase] = max(0, repetitive_phrases[phrase] - 1)

max_seq_len = 40
train_messages = 2500
test_messages = 2500
epochs = 1500
nodes = 64
nodes2 = 32
nodes3 = 32

make_fake_messages(train_messages + test_messages)

def make_message_class(text, good):
	msg = Message(":0:abc:{0}".format(text))
	msg.label = LABELS['Discussion'] if good else LABELS['Repetitive']
	return msg

ArtificialDatasetFactory.NUM_MESSAGES = train_messages + test_messages
ads_factory = ArtificialDatasetFactory()
artificial_improved = map(lambda (msg, label): make_message_class(msg, label), zip(ads_factory.messages, ads_factory.labels))

messages = artificial_improved

classified_messages = [msg for msg in messages if msg.label in (good_labels + [LABELS['Repetitive']])][:train_messages + test_messages]
for msg in classified_messages:
    make_ascii(msg)
    ignore_caps(msg)     
    
reduced_messages = [msg for msg in classified_messages if msg.label in [LABELS['Repetitive'], LABELS['Discussion']]]

#import pdb; pdb.set_trace()

X = [([ord(c) for c in msg.message] + [-1.]) for msg in classified_messages]
X = pad_sequences(X, maxlen=max_seq_len, dtype='float32')
X = np.reshape(X, (X.shape[0], max_seq_len, 1)) 
X = X / np.linalg.norm(X)
y = np.array([(int(msg.label != LABELS['Repetitive'])) for msg in classified_messages])

X_tr = X[:train_messages]
y_tr = y[:train_messages]
X_te = X[train_messages:train_messages + test_messages]
y_te = y[train_messages:train_messages + test_messages]


def train():
    model = Sequential()
    model.add(GRU(nodes, batch_input_shape=(1, X_tr.shape[1], X_tr.shape[2]), stateful=True, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(GRU(nodes2, return_sequences=True, stateful=True))
    model.add(Dropout(0.2))
    model.add(GRU(nodes3, stateful=True))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))

	# usually lr=0.0001
    model.compile(loss='binary_crossentropy', optimizer=Adam(lr=0.0001), metrics=['accuracy'])

    for i in xrange(epochs):
        model.fit(X_tr, y_tr, nb_epoch=1, batch_size=1, verbose=1, shuffle=False)
        model.reset_states()
        print 'EPOCH {0}'.format(i)
        if i % 10 == 0:
			score_string_tr = evaluate(model, X_tr, y_tr)
			score_string_te = evaluate(model, X_te, y_te)
			with open(os.getcwd() + '/scores.txt'.format(i), 'a') as f:
				f.write(str(i))
				f.write(score_string_tr)
				f.write(score_string_te)
				f.write('\n')
			model.save('interim')
        
    evaluate(model, X_tr, y_tr)
    model.reset_states()

    model.save('model1')
    return model

def load():
    return load_model('model1')
    
def continue_training(model):
    for i in xrange(epochs):
        model.fit(X_tr, y_tr, nb_epoch=1, batch_size=1, verbose=1, shuffle=False)
        model.reset_states()
        print 'EPOCH {0}'.format(i)
        if i % 100 == 0:
			score_string_tr = evaluate(model, X_tr, y_tr)
			score_string_te = evaluate(model, X_te, y_te)
			with open(os.getcwd() + '/scores.txt'.format(i), 'a') as f:
				f.write(str(i))
				f.write(score_string_tr)
				f.write(score_string_te)
				f.write('\n')
			model.save('interim')
        
    evaluate(model, X_tr, y_tr)
    model.reset_states()

    model.save('model1')
    return model
    
def evaluate(model, X_eval, y_eval):
    model.reset_states()
    scores = model.evaluate(X_eval, y_eval, batch_size=1, verbose=0)
    model.reset_states()
    predicts = model.predict(X_eval[:100], batch_size=1)
    for msg, predict in zip(classified_messages[:100], predicts):
        print msg.message 	 	
        print predict
    score_string = "Model Accuracy: %.2f%%" % (scores[1]*100)
    print(score_string)
    return score_string
  
trained_model = train() 
#trained_model = load()
#continue_training(trained_model)
print "Train set:"
evaluate(trained_model, X_tr, y_tr)
print "\n\nTest set:"
evaluate(trained_model, X_te, y_te)

with open(os.getcwd() + '/fake_set.pkl', 'wb') as f:
    pickle.dump(artificial_improved, f) 

