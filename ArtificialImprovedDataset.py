import random


class Alphabet:
    CHAR_DIST = 'aeiouabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+=-/?.>,<'
    LENGTH = len(CHAR_DIST)


class RepetitivePhrase:
    def __init__(self, reset_rate, spelling_change_ratio, phrase_change_ratio):
        self.messages_since_last_seen = reset_rate
        self.spelling_change_ratio = spelling_change_ratio
        self.phrase_change_ratio = phrase_change_ratio
        self.message = ArtificialImprovedDatasetFactory.get_message(True)

    def get_specific_instance(self):
        start = self.message
        while random.randint(0, 99) < self.spelling_change_ratio * 100:
            start = self.mutate_spelling(start)

        while random.randint(0, 99) < self.phrase_change_ratio * 100:
            start = self.mutate_phrase(start)
        return start

    @staticmethod
    def mutate_spelling(starter):
        c_dist = ArtificialImprovedDatasetFactory.CHAR_DISTRIBUTION_REPETITIVE
        distributor = random.randint(0, 99) / 100.0
        new_char = 'e'
        for (char, prob) in c_dist.iteritems():
            distributor -= prob
            if distributor <= 0:
                new_char = char
                break

        existing_char = ' '
        while existing_char == ' ' and len(starter) > 0:
            swap_pos = random.randint(0, len(starter) - 1)
            existing_char = starter[swap_pos]
        starter = list(starter)
        starter[swap_pos] = new_char
        return ''.join(starter)

    @staticmethod
    def mutate_phrase(starter):
        words = starter.split()
        position = random.randint(0, len(words))
        new_word = ArtificialImprovedDatasetFactory.get_word(True)
        words.insert(position, new_word)
        return reduce(lambda a, b: a + ' ' + b, words)[:-1]


class ArtificialImprovedDatasetFactory:
    NUM_MESSAGES = 5000
    REPETITIVE_PHRASE_EACH = 150
    REPETITIVE_RATIO = 0.625840017342
    REPETITIVE_SPELLING_CHANGE = 0.15
    REPETITIVE_PHRASE_CHANGE = 0.15
    REPETITIVE_RESET_RATE = 40
    WORD_COUNT_DISTRIBUTION_REPETITIVE = {1: 0.6172497402147558, 2: 0.13785936958780742, 3: 0.0914444059577416, 4: 0.051264288188430894, 5: 0.04399030135088327, 6: 0.02216834083824039, 7: 0.018011776931070315, 8: 0.011084170419120194, 9: 0.004502944232767579, 10: 0.0020782819535850364, 11: 0.00034638032559750607}
    WORD_COUNT_DISTRIBUTION_DISC = {1: 0.313441483198146, 2: 0.15585168018539977, 3: 0.13557358053302435, 4: 0.10602549246813442, 5: 0.07589803012746234, 6: 0.06836616454229433, 7: 0.04982618771726535, 8: 0.054461181923522596, 9: 0.02433371958285052, 10: 0.013904982618771726, 11: 0.0011587485515643105, 12: 0.0011587485515643105}

    WORD_LENGTH_DISTRIBUTION_REPETITIVE = {0: 0.003109345310070824, 1: 0.028329590602867508, 2: 0.05596821558127483, 3: 0.08049749524961133, 4: 0.1385386077042667, 5: 0.162204180342028, 6: 0.2724131974434272, 7: 0.03558472965969943, 8: 0.08067023665572638, 9: 0.07116945931939886, 10: 0.02487476248056659, 11: 0.012955605458628434, 12: 0.00984626014855761, 13: 0.00449127655899119, 14: 0.0008637070305752289, 15: 0.006391432026256694, 16: 0.007600621869062014, 17: 0.0005182242183451373, 18: 0.0005182242183451373, 19: 0.00034548281223009154, 20: 0.00034548281223009154, 21: 0.0006909656244601831, 23: 0.0006909656244601831, 24: 0.00017274140611504577, 25: 0.00034548281223009154, 26: 0.00017274140611504577, 27: 0.00017274140611504577, 28: 0.00017274140611504577, 39: 0.00017274140611504577, 40: 0.00017274140611504577}
    WORD_LENGTH_DISTRIBUTION_DISC = {0: 0.0067865626060400405, 1: 0.0495419070240923, 2: 0.12453342382083475, 3: 0.17288768238887003, 4: 0.18781812012215812, 5: 0.12351543942992874, 6: 0.1016287750254496, 7: 0.07838479809976247, 8: 0.04665761791652528, 9: 0.039362063115032236, 10: 0.029691211401425176, 11: 0.01510010179843909, 12: 0.010349507974211062, 13: 0.004241601628775025, 14: 0.002205632846963013, 15: 0.002205632846963013, 16: 0.0018663047166610112, 17: 0.0008483203257550051, 18: 0.00016966406515100103, 19: 0.00016966406515100103, 20: 0.0005089921954530031, 21: 0.00016966406515100103, 22: 0.00033932813030200206, 25: 0.00016966406515100103, 26: 0.00016966406515100103, 27: 0.00016966406515100103, 28: 0.00016966406515100103, 29: 0.00016966406515100103, 33: 0.00016966406515100103}

    CHAR_DISTRIBUTION_REPETITIVE =  {u'\x01': 2.9862334637321945e-05, u'\r': 0.08068802819004389, u'!': 0.004897422880520799, u'#': 8.958700391196584e-05, u'"': 2.9862334637321945e-05, u'$': 0.003882103502851853, u"'": 0.00041807268492250724, u'&': 5.972466927464389e-05, u')': 0.0003284856810105414, u'(': 0.00011944933854928778, u'+': 5.972466927464389e-05, u'*': 0.0008062830352076925, u'-': 0.00020903634246125362, u',': 0.00035834801564786335, u'/': 0.0008660077044823364, u'.': 0.0020306387553378925, u'1': 0.0040911398453131066, u'0': 0.008182279690626213, u'3': 0.00026876101173589753, u'2': 0.0009257323737569803, u'5': 0.005076596888344731, u'4': 0.0005375220234717951, u'7': 0.000567384358109117, u'6': 0.0008958700391196584, u'9': 8.958700391196584e-05, u'8': 5.972466927464389e-05, u'=': 8.958700391196584e-05, u'?': 0.0010153193776689462, u'>': 5.972466927464389e-05, u'@': 0.00041807268492250724, u'\\': 0.00023889867709857556, u'_': 0.00011944933854928778, u'a': 0.15549317645653538, u'c': 0.025024636426075792, u'b': 0.009764983426404276, u'e': 0.061008749664048734, u'd': 0.031325589034550724, u'g': 0.0322513214083077, u'f': 0.006062053931376355, u'i': 0.025382984441723655, u'h': 0.03240063308149431, u'k': 0.06969868904350943, u'j': 0.0013438050586794875, u'm': 0.025830919461283484, u'l': 0.0450324006330815, u'o': 0.057335682503658135, u'n': 0.0315644877116493, u'q': 0.007196822647594589, u'p': 0.15695643085376415, u's': 0.02810045689371995, u'r': 0.017290291755009405, u'u': 0.016484008719801713, u't': 0.03284856810105414, u'w': 0.004628661868784902, u'v': 0.0017917400782393167, u'y': 0.006659300624122794, u'x': 0.00017917400782393168, u'z': 0.0008361453698450145}
    CHAR_DISTRIBUTION_DISC =        {u'\x01': 0.0001741614127973806, u'\r': 0.05228325612177366, u'!': 0.007976592706120032, u'#': 0.00010449684767842837, u'"': 0.0005921488035110941, u'%': 0.0001393291302379045, u'$': 0.0001741614127973806, u"'": 0.0021596015186875197, u')': 0.0009404716291058553, u'(': 0.0005224842383921419, u'+': 0.00024382597791633285, u'*': 0.0016371172802953778, u'-': 0.0003134905430352851, u',': 0.0027865826047580896, u'/': 0.0005921488035110941, u'.': 0.0023685952140443762, u'1': 0.0024034274966038523, u'0': 0.0029955763001149466, u'3': 0.0010798007593437599, u'2': 0.0018809432582117106, u'5': 0.0014629558674979972, u'4': 0.0018461109756522345, u'7': 0.0016371172802953778, u'6': 0.0013932913023790448, u'9': 0.0005224842383921419, u'8': 0.00020899369535685674, u'=': 0.00024382597791633285, u'<': 0.0003134905430352851, u'?': 0.004249538472256087, u'>': 0.00024382597791633285, u'@': 0.003134905430352851, u'\\': 0.0003134905430352851, u'_': 0.0004179873907137135, u'^': 6.966456511895225e-05, u'a': 0.07903444912745132, u'`': 3.483228255947612e-05, u'c': 0.024730920617228046, u'b': 0.016475669650632206, u'e': 0.09383816921522867, u'd': 0.03396147549548922, u'g': 0.02769166463478352, u'f': 0.01302727367724407, u'i': 0.061304817304677975, u'h': 0.04064927374690863, u'k': 0.020446549862412483, u'j': 0.002542756626841757, u'm': 0.031105228325612178, u'l': 0.04434149569821311, u'o': 0.06820160925145424, u'n': 0.05172593960082204, u'q': 0.010136194224807552, u'p': 0.03685255494792574, u's': 0.05510467100909123, u'r': 0.03845483994566164, u'u': 0.030234421261625274, u't': 0.07621303424013376, u'w': 0.01591835312968059, u'v': 0.006896791946776272, u'y': 0.019819568776341914, u'x': 0.0016022849977359015, u'z': 0.002194433801246996, u'|': 3.483228255947612e-05}

    MEAN_WORD_LENGTH = 4
    REPETITIVE_PHRASE_WINDOW = 10

    def __init__(self):
        self.repetitive_phrases = []
        for i in xrange(self.NUM_MESSAGES / self.REPETITIVE_PHRASE_EACH):
            self.repetitive_phrases += [RepetitivePhrase(self.REPETITIVE_RESET_RATE, self.REPETITIVE_SPELLING_CHANGE,
                                                         self.REPETITIVE_PHRASE_CHANGE)]
        self.messages = []
        self.labels = []
        for i in xrange(self.NUM_MESSAGES):
            msg, label = self.generate_message(i)
            self.messages += [msg]
            self.labels += [label]
            for phrase in self.repetitive_phrases:
                phrase.messages_since_last_seen += 1

    def generate_message(self, message_num):
        if random.randint(0, 99) < self.REPETITIVE_RATIO * 100:
            phrase_index = min(len(self.repetitive_phrases) - 1, max(0, random.randint(-5, 5) + (message_num / self.REPETITIVE_PHRASE_EACH)))
            phrase = self.repetitive_phrases[phrase_index]
            instance = (phrase.get_specific_instance(), phrase.messages_since_last_seen >= self.REPETITIVE_RESET_RATE)
            phrase.messages_since_last_seen = 0
            return instance
        else:
            return self.get_message(False), True

    @staticmethod
    def get_word_count(repetitive):
        wc_distr = ArtificialImprovedDatasetFactory.WORD_COUNT_DISTRIBUTION_REPETITIVE if repetitive else ArtificialImprovedDatasetFactory.WORD_COUNT_DISTRIBUTION_DISC
        distributor = random.randint(0, 99) / 100.0
        for (length, prob) in wc_distr.iteritems():
            distributor -= prob
            if distributor <= 0:
                return length
        return max(wc_distr.keys())

    @staticmethod
    def get_word(repetitive):
        wl_distr = ArtificialImprovedDatasetFactory.WORD_LENGTH_DISTRIBUTION_REPETITIVE if repetitive else ArtificialImprovedDatasetFactory.WORD_LENGTH_DISTRIBUTION_DISC
        distributor = random.randint(0, 99) / 100.0
        length = max(wl_distr.keys())
        for (chars, prob) in wl_distr.iteritems():
            distributor -= prob
            if distributor <= 0:
                length = chars
                break

        word = ''
        for i in xrange(length):
            c_dist = ArtificialImprovedDatasetFactory.CHAR_DISTRIBUTION_REPETITIVE if repetitive else ArtificialImprovedDatasetFactory.CHAR_DISTRIBUTION_DISC
            distributor = random.randint(0, 99) / 100.0
            next_char = 'e'
            for (char, prob) in c_dist.iteritems():
                distributor -= prob
                if distributor <= 0:
                    next_char = char
                    break

            word += next_char
        return word

    @staticmethod
    def get_message(repetitive):
        word_count = ArtificialImprovedDatasetFactory.get_word_count(repetitive)
        message = ''
        for count in xrange(word_count):
            message += ArtificialImprovedDatasetFactory.get_word(repetitive) + ' '
        return message[:-1]

ArtificialImprovedDatasetFactory.NUM_MESSAGES = 350
ads = ArtificialImprovedDatasetFactory()
for msg in ads.messages:
    print msg
