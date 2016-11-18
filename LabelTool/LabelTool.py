from __future__ import unicode_literals
import codecs
import os
import pickle
from Message import Message, LABELS


PICKLED_MESSAGES = os.getcwd() + '/data/messages.pkl'
RAW_MESSAGE_STRINGS = os.getcwd() + '/data/raw_dataset.txt'


def parse_messages():
    with codecs.open(RAW_MESSAGE_STRINGS, 'r', 'utf-8') as f:
        lines = f.readlines()
    messages = []

    for line in lines:
        try:
            messages += [Message(line)]
        except ValueError:
            pass  # ignore messages with errors
    return messages


input_label_map = {
    'g':    'Good',
    'b':    'Bad',
    'r':    'Repetitive',
    'o':    'Offensive',
    'l':    'Link',
    'd':    'Discussion',
    'e':    'Endorsed Automated',
    'n':    'Non-English'
}


def label_message(message):
    while True:
        if message.label == LABELS['Unknown']:
            prompt = '(b)ad or (g)ood'
        elif message.label == LABELS['Bad']:
            prompt = '(r)epetitive or (o)ther'
        elif message.label == LABELS['Good']:
            prompt = '(d)iscussion or (e)ndorsed automated'

        answer = raw_input(prompt)
        if answer == 'o':
            answer = raw_input('(n)on-english, (o)ffensive, or (l)ink')
        if answer == 'q':
            return False
        try:
            message.label = LABELS[input_label_map[answer]]
            return True
        except KeyError:
            pass

if not os.path.isfile(PICKLED_MESSAGES):

    messages = parse_messages()
else:
    with open(PICKLED_MESSAGES, 'rb') as f:
        messages = pickle.load(f)

unknown_count = len([message for message in messages if message.label == LABELS['Unknown']])
bad_count = len([message for message in messages if message.label == LABELS['Bad']])
good_count = len([message for message in messages if message.label == LABELS['Good']])

print "There are {0} labelled messages, {1} bad messages needing more clarification, and {2} good messages needing more clarification." \
    .format(len(messages) - unknown_count, bad_count, good_count)
answer = raw_input('Do you want to classify (u)nknown messages, (g)ood messages, or (b)ad messages?')

classify_label = LABELS['Good' if answer == 'g' else ('Bad' if answer == 'b' else 'Unknown')]
count_target = good_count if answer == 'g' else (bad_count if answer == 'b' else unknown_count)

labelled_count = 0
for message in messages:
    print "{0}: {1}".format(message.username, message.message)
    if message.label == classify_label:
        labelled_count += 1
        do_not_quit = label_message(message)
        if labelled_count == count_target:
            print 'All messages in this category are now labelled.'
            do_not_quit = False
        if not do_not_quit:
            print 'Saving and exiting...'
            with open(PICKLED_MESSAGES, "wb") as f:
                pickle.dump(messages, f)
            exit(0)
