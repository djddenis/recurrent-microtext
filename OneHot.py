from operator import add
import numpy as np


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
