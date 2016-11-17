import random


class Alphabet:
    CHAR_DIST = 'aeiouabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+=-/?.>,<'
    LENGTH = len(CHAR_DIST)


class RepetitivePhrase:
    def __init__(self, reset_rate, spelling_change_ratio, phrase_change_ratio):
        self.messages_since_last_seen = reset_rate
        self.spelling_change_ratio = spelling_change_ratio
        self.phrase_change_ratio = phrase_change_ratio
        self.message = ArtificialDatasetFactory.get_message()

    def get_specific_instance(self):
        start = self.message
        while random.randint(0, 99) < self.spelling_change_ratio * 100:
            start = self.mutate_spelling(start)

        while random.randint(0, 99) < self.phrase_change_ratio * 100:
            start = self.mutate_phrase(start)
        return start

    @staticmethod
    def mutate_spelling(starter):
        new_char = Alphabet.CHAR_DIST[random.randint(0, Alphabet.LENGTH - 1)]
        existing_char = ' '
        while existing_char == ' ':
            swap_pos = random.randint(0, len(starter) - 1)
            existing_char = starter[swap_pos]
        starter = list(starter)
        starter[swap_pos] = new_char
        return ''.join(starter)

    @staticmethod
    def mutate_phrase(starter):
        words = starter.split()
        position = random.randint(0, len(words))
        new_word = ArtificialDatasetFactory.get_word()
        words.insert(position, new_word)
        return reduce(lambda a, b: a + ' ' + b, words)[:-1]


class ArtificialDatasetFactory:
    NUM_MESSAGES = 5000
    REPETITIVE_PHRASE_EACH = 150
    REPETITIVE_RATIO = 0.7
    REPETITIVE_SPELLING_CHANGE = 0.1
    REPETITIVE_PHRASE_CHANGE = 0.1
    REPETITIVE_RESET_RATE = 40
    WORD_COUNT_DISTRIBUTION = [50, 10, 10, 5, 3, 2, 1, 1, 1, 1, 1, 5, 5, 5, 5]
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
            return self.get_message(), True

    @staticmethod
    def get_word_count():
        distributor = random.randint(0, 99)
        for (length, prob) in enumerate(ArtificialDatasetFactory.WORD_COUNT_DISTRIBUTION, start=1):
            distributor -= prob
            if distributor <= 0:
                return length

    @staticmethod
    def get_word():
        length = ArtificialDatasetFactory.MEAN_WORD_LENGTH + random.randint(-3, 3)
        word = ''
        for char in xrange(length):
            word += Alphabet.CHAR_DIST[random.randint(0, Alphabet.LENGTH - 1)]
        return word

    @staticmethod
    def get_message():
        word_count = ArtificialDatasetFactory.get_word_count()
        message = ''
        for count in xrange(word_count):
            message += ArtificialDatasetFactory.get_word() + ' '
        return message[:-1]
