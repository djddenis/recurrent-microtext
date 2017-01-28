from __future__ import unicode_literals

import pickle
import os
from operator import add, itemgetter
from Message import Message, LABELS
import matplotlib.pyplot as plt
import numpy as np

max_seq_len = 40


with open(os.getcwd() + '/messages.pkl', 'rb') as f:
    messages = pickle.load(f)

word_counts_overall = dict()
word_counts_non = dict()
word_counts_rep = dict()
total = 0
total_disc = 0
total_repetitive = 0
total_labelled_but_not_repetitive = 0

word_lengths_rep = dict()
word_lengths_dis = dict()
words_total_rep = 0
words_total_dis = 0

char_counts_rep = dict()
char_counts_dis = dict()
char_totals_rep = 0
char_totals_dis = 0

message_lengths = dict()

users = set()
for msg in messages:
    msg.make_ascii()
    msg.ignore_caps()
    msg_len = len(msg.message)
    if msg_len in message_lengths:
        message_lengths[msg_len] += 1
    else:
        message_lengths[msg_len] = 1
    users.add(msg.username)
    considered = msg.message[0:40]
    total += 1
    words = len(considered.split(' '))
    if words in word_counts_overall:
        word_counts_overall[words] += 1.
    else:
        word_counts_overall[words] = 1.

    if msg.label == LABELS['Repetitive']:
        total_repetitive += 1
        if words in word_counts_rep:
            word_counts_rep[words] += 1.
        else:
            word_counts_rep[words] = 1.
    elif msg.label == LABELS['Discussion']:
        total_disc += 1
        if words in word_counts_non:
            word_counts_non[words] += 1.
        else:
            word_counts_non[words] = 1

    if msg.label != LABELS['Unknown'] and msg.label != LABELS['Repetitive']:
        total_labelled_but_not_repetitive += 1
            
    for word in considered.split(" "):
        chars = len(word)
        if msg.label == LABELS['Repetitive']:
            words_total_rep += 1
            if chars in word_lengths_rep:
                word_lengths_rep[chars] += 1.
            else:
                word_lengths_rep[chars] = 1.
        if msg.label == LABELS['Discussion']:
            words_total_dis += 1
            if chars in word_lengths_dis:
                word_lengths_dis[chars] += 1.
            else:
                word_lengths_dis[chars] = 1.

        for char in word:
            if msg.label == LABELS['Repetitive']:
                char_totals_rep += 1
                if char in char_counts_rep:
                    char_counts_rep[char] += 1.
                else:
                    char_counts_rep[char] = 1.
            if msg.label == LABELS['Discussion']:
                char_totals_dis += 1
                if char in char_counts_dis:
                    char_counts_dis[char] += 1.
                else:
                    char_counts_dis[char] = 1.


for words in word_counts_overall.keys():
    word_counts_overall[words] /= total
for words in word_counts_rep.keys():
    word_counts_rep[words] /= total_repetitive
for words in word_counts_non.keys():
    word_counts_non[words] /= total_disc

for chars in word_lengths_rep.keys():
    word_lengths_rep[chars] /= words_total_rep
for chars in word_lengths_dis.keys():
    word_lengths_dis[chars] /= words_total_dis

for char in char_counts_rep.keys():
    char_counts_rep[char] /= char_totals_rep
for char in char_counts_dis.keys():
    char_counts_dis[char] /= char_totals_dis

print "users: {}".format(len(users))
print "word count distributions:"
print word_counts_overall
print word_counts_rep
print word_counts_non

print "word length distributions"
print word_lengths_rep
rep_03 = word_lengths_rep[0] + word_lengths_rep[1] + word_lengths_rep[2] + word_lengths_rep[3]
rep_46 = word_lengths_rep[4] + word_lengths_rep[5] + word_lengths_rep[6]
print "0-3: {}, 4-6: {}, 7+: {}".format(rep_03, rep_46, 1.0 - rep_03 - rep_46)
print word_lengths_dis
dis_03 = word_lengths_dis[0] + word_lengths_dis[1] + word_lengths_dis[2] + word_lengths_dis[3]
dis_46 = word_lengths_dis[4] + word_lengths_dis[5] + word_lengths_dis[6]
print "0-3: {}, 4-6: {}, 7+: {}".format(dis_03, dis_46, 1.0 - dis_03 - dis_46)

print "char distributions"
print char_counts_rep
print sum(char_counts_rep.values())
print char_counts_dis
print sum(char_counts_dis.values())

sorted_rep = sorted(char_counts_rep.iteritems(), key=lambda (k, v): v, reverse=True)
sorted_dis = sorted(char_counts_dis.iteritems(), key=lambda (k, v): v, reverse=True)

interesting_chars = list(set([key for key, _ in sorted_rep[:10]]).union(set([key for key, __ in sorted_dis[:10]])))
interesting_chars = [char for char in interesting_chars if char != "\r"]
interesting_chars = sorted(interesting_chars, key=lambda c: max(char_counts_rep[c], char_counts_dis[c]), reverse=True)

# ind = np.arange(len(interesting_chars))
# fig, ax = plt.subplots()
# rects1 = ax.bar(ind, [char_counts_rep[char] for char in interesting_chars], 0.35, color='r')
# rects2 = ax.bar(ind + 0.35, [char_counts_dis[char] for char in interesting_chars], 0.35, color='b')
#
# ax.set_ylabel('Probability')
# ax.set_title('Likeliest Characters')
# ax.set_xticks(ind + 0.35)
# ax.set_xticklabels(interesting_chars)
# ax.legend((rects1[0], rects2[0]), ('Repetitive', 'Non-Repetitive'))
#
# # plt.show()

print "proportion repetitive in reduced dataset"
print float(total_repetitive) / (total_repetitive + total_disc)

print "proportion repetitive in full dataset"
print float(total_repetitive) / (total_repetitive + total_labelled_but_not_repetitive)

print "message lengths"

msg_texts = [msg.message for msg in messages]
unique_count = len(set(msg_texts))
same_at = dict()
for i in xrange(5, 30):
    same_at[i] = float(unique_count - len(set([msg[:i] for msg in msg_texts]))) / total

print unique_count
print same_at

stuff = [(blue, stu) for blue, stu in sorted(same_at.iteritems(), key=lambda (k,v): k)]
blue = [blu for blu, stu in stuff]
stue = [stu for blu, stu in stuff]

fig, ax = plt.subplots()
rects1 = ax.bar(blue, stue, color='r')

ax.set_ylabel('Percentage of Dataset Made Indistinguishable')
ax.set_xlabel('Crop Length')
ax.set_title('Crop Length Effect on Dataset')

plt.show()

# so_far = 0
# median = 0
# for i in message_lengths.keys():
#     so_far += message_lengths[i]
#     if so_far > float(total) / 2:
#         median = i
#         break
#
# mean = 0.
# for (len, count) in message_lengths.iteritems():
#     mean += (float(count) * len) / total
#
# cropped_ratios = dict()
# for i in range(30, 100):
#     cropped_ratios[i] = float(sum(count for (len, count) in message_lengths.iteritems() if len > i)) / total
#
# print "mean {}".format(mean)
# print "median {}".format(median)
# print "cropped {}".format(cropped_ratios)
#
# cropped_ratio_jumps = dict()
# for len, ratio in cropped_ratios.iteritems():
#     next = cropped_ratios[len + 1] if len + 1 in cropped_ratios else 0
#     cropped_ratio_jumps[len] = ratio - next
# print "cropped ratio jumps {}".format(cropped_ratio_jumps)
#
# filtered_lengths = []
# for leng, count in message_lengths.iteritems():
#     if leng < 200:
#         for i in xrange(0, count):
#             filtered_lengths += [leng]
#
# array_lengths = np.array(filtered_lengths)
#
# n, bins, patches = plt.hist(array_lengths, 100)
#
# plt.xlabel('Message Length')
# plt.ylabel('Count')
# plt.title('Message Lengths Histogram')
# # plt.axis([40, 160, 0, 0.03])
# # plt.grid(True)
#
# plt.show()

