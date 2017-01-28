from __future__ import unicode_literals

import numpy as np
import pickle
import os
from ArtificialImprovedDataset import ArtificialImprovedDatasetFactory
from Message import Message, LABELS
from Encodings import get_one_hot, get_c2v_encoded, C2V_ENCODING_SIZE
import BasicArtificialDataset
from sklearn.linear_model import SGDClassifier

with open(os.getcwd() + '/messages.pkl', 'rb') as f:
    messages = pickle.load(f)

max_seq_len = 40
train_messages = 2500
test_messages = 2500
epochs = 20000

# Basic artificial dataset
BasicArtificialDataset.make_fake_messages(train_messages + test_messages)
basic_artificial = BasicArtificialDataset.fake_messages


# Artificial improved dataset
def make_message_class(text, good):
    msg = Message(":0:abc:{0}".format(text))
    msg.label = LABELS['Discussion'] if good else LABELS['Repetitive']
    return msg

ArtificialImprovedDatasetFactory.REPETITIVE_RESET_RATE = 10
ArtificialImprovedDatasetFactory.NUM_MESSAGES = train_messages + test_messages
ads_factory = ArtificialImprovedDatasetFactory()
artificial_improved = map(lambda (msg, label): make_message_class(msg, label), zip(ads_factory.messages, ads_factory.labels))

# Real datset
real_dataset = [msg for msg in messages if msg.label != LABELS['Unknown']][:train_messages + test_messages]

# Reduced dataset
reduced_real = [msg for msg in real_dataset if msg.label in [LABELS['Repetitive'], LABELS['Discussion'], LABELS['Good'], LABELS['Endorsed Automated']]]

done = False
while not done:
    done = True
    ds_answer = raw_input('Use (r)eal dataset, re(d)uced real dataset, (b)asic artificial dataset, or artificial (i)mproved dataset?').lower()
    if ds_answer == 'r':
        messages = real_dataset
    elif ds_answer == 'd':
        messages = reduced_real
        test_messages = min(test_messages, len(messages) - train_messages)
    elif ds_answer == 'b':
        messages = basic_artificial
    elif ds_answer == 'i':
        messages = artificial_improved
        with open(os.getcwd() + '/fake_set.pkl', 'wb') as f:
            pickle.dump(artificial_improved, f)
    else:
        done = False

for msg in messages:
    msg.make_ascii()
    msg.ignore_caps()
    msg.fix_length(max_seq_len)

X = get_one_hot(messages)
X = X.reshape(train_messages + test_messages, X.shape[1] * (max_seq_len + 1))
y = np.array([(int(msg.label != LABELS['Repetitive'])) for msg in messages])

X_tr = X[:train_messages]
y_tr = y[:train_messages]
X_te = X[train_messages:train_messages + test_messages]
y_te = y[train_messages:train_messages + test_messages]

print('Begin training')

reg = SGDClassifier(loss='log', penalty='l1', class_weight='balanced')
reg.fit(X_tr, y_tr)
train_predict = reg.predict(X_tr)
test_predict = reg.predict(X_te)

train_acc = 1.0 - (np.count_nonzero(y_tr - train_predict) / float(y_tr.shape[0]))
test_acc = 1.0 - (np.count_nonzero(y_te - test_predict) / float(y_te.shape[0]))

disc_ratio_train = sum(y_tr) / float(y_tr.shape[0])
disc_ratio_test = sum(y_te) / float(y_te.shape[0])

print "Train acc: {}, Test acc: {}".format(train_acc, test_acc)
print "Train base: {}, Test base: {}".format(max(1.0 - disc_ratio_train, disc_ratio_train), max(1.0 - disc_ratio_test, disc_ratio_test))

for i in range(0, 100):
    print ''.join([c for c in messages[i].message if c != chr(0)])
    print 1 - train_predict[i]
