from operator import add
import numpy as np
import os


def get_one_hot(messages):
    msg_contents = [msg.message for msg in messages]
    all_msg_text = reduce(add, msg_contents)
    used_chars = list(set(all_msg_text))
    lookup = dict(zip(used_chars, range(0, len(used_chars))))

    full_so_far = None
    for msg in messages:
        mat = np.zeros((len(msg.message) + 1, len(used_chars) + 1))  # +1s are for the 'end of message' character
        for i, char in enumerate(msg.message):
            mat[i][lookup[char]] = 1
        mat[-1][len(used_chars)] = 1  # add 'end of message' character
        if full_so_far is not None:
            full_so_far = np.vstack((full_so_far, mat))
        else:
            full_so_far = mat
    return full_so_far

C2V_ENCODING_SIZE = 16


def get_c2v_encoded(messages):
    encoding = load_c2v_encoding()

    full_so_far = None
    for msg in messages:
        msg.message += '\r'
        mat = np.zeros((len(msg.message), C2V_ENCODING_SIZE))
        for i, char in enumerate(msg.message):
            mat[i] = np.array(encoding[char])
        if full_so_far is not None:
            full_so_far = np.vstack((full_so_far, mat))
        else:
            full_so_far = mat
    return full_so_far


def load_c2v_encoding():
    encoding = dict()
    with open(os.getcwd() + '/c2v_vec.txt', 'r+') as f:
        for line in f.readlines()[1:]:
            pieces = line.split(' ')
            char = pieces[0]
            vec = [float(i) for i in pieces[1: C2V_ENCODING_SIZE + 1]]
            if char == '</s>':
                char = '\r'
            if char == 'S':
                char = ' '
            encoding[char] = vec
    encoding[chr(0)] = np.zeros(C2V_ENCODING_SIZE)
    # encoding['|'] = np.zeros(C2V_ENCODING_SIZE)
    return encoding