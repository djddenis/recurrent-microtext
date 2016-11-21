import os
import pickle
from Message import Message, LABELS

with open(os.getcwd() + '/messages.pkl', 'rb') as f:
    messages = pickle.load(f)

with open(os.getcwd() + '/sample_data.txt', 'w') as fw:
    for msg in messages:
        msg.make_ascii()
        msg.ignore_caps()
        if msg.label != LABELS['Unknown']:
            fw.write(msg.username + ': ' + msg.message)
