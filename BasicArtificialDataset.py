from Message import Message, LABELS
import random

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