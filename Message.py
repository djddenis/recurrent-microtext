from operator import add

LABELS = {
    'Unknown':              (-1),
    'Bad':                  (-2),
    'Good':                 (-3),
    'Discussion':           0,
    'Endorsed Automated':   1,
    'Repetitive':           2,
    'Offensive':            3,
    'Link':                 4,
    'Non-English':          5,
    }


class Message:
    def __init__(self, raw_string):
        parts = raw_string.split(':')

        if len(parts) < 4:
            if 'PING' in raw_string:
                error = 'PING message'
            elif 'DECODE ERROR' in raw_string:
                error = 'Unicode error in message'
            else:
                error = 'Invalid message format'
            raise ValueError(error)

        self.timestamp = int(parts[1].strip(': '))
        self.username = parts[2].split('!')[0].strip(':! ')
        self.message = reduce(add, parts[3:]).strip('\n')
        self.label = LABELS['Unknown']

    def make_ascii(self):
        self.message = self.message.encode('ascii', 'ignore')

    def ignore_caps(self):
        self.message = self.message.lower()

    def fix_length(self, length):
        if len(self.message) >= length:
            self.message = self.message[0:length]
        else:
            self.message += "".join([chr(0)] * (length - len(self.message)))
