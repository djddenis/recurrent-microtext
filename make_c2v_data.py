from __future__ import unicode_literals

import pickle
import os
from operator import add
from Message import Message, LABELS

max_seq_len = 40


with open(os.getcwd() + '/messages.pkl', 'rb') as f:
    messages = pickle.load(f)

with open(os.getcwd() + '/c2v_data.txt', 'w') as f:
    for msg in messages:
        msg.make_ascii()
        msg.ignore_caps()
        msg.fix_length(max_seq_len)
        
        temp = msg.message + '\r'
        temp = temp.replace(' ', 'S')
        temp = zip(temp, [' '] * len(temp))
        msg.message = "".join(reduce(add, temp)) 
        f.write(msg.message)
