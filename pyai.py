import random
import marshal
from os.path import isfile

voyelles = 'aÃ Ã¢eÃ©Ã¨ÃªiÃ®Ã¯oÃ¶Ã´uÃ¼Ã»y'
sentence_ends = ['.', '?', '!']

class PyAI:

    def __init__(self, db_file='ai.db'):
        self.db_file = db_file
        self.lines = {}
        self.words = {}
        self.min_context_depth = 5
        self.max_context_depth = 10
        self.load_db()

    def load_db(self):
        if isfile(self.db_file):
            print('loading database...')
            with open(self.db_file, 'rb') as f:
                self.lines = marshal.load(f)
                self.words = marshal.load(f)
        else:
            print('No database found!')

    def save_db(self):
        with open(self.db_file, 'wb') as f:
            marshal.dump(self.lines, f)
            marshal.dump(self.words, f)

    def is_valid(self, word):
        for c in word:
            num_voy = 0
            num_digits = 0
            num_chars = 0
            if c in voyelles:
                num_voy += 1
            elif c.isalpha():
                num_digits += 1
            elif c.isdigit():
                num_chars += 1

        # if word > 13 chars
        # or less than 25% voyels
        # or digits and chars in the word
        if len(word) > 13 or \
            (((num_voy * 100) / len(word) < 26) and len(word) > 5)\
                or (num_chars and num_digits):
            return False
        return True

    def filter_split_message(self, msg):
        '''
        filter message (delete some words, correct sentence-endings) and split
        '''
        for sentence_end in sentence_ends:
            msg = msg.replace(sentence_end, ' . ')
        sentences = []
        for sentence in msg.split(' . '):
            sentences.append(' '.join(word for word in sentence.split() if self.is_valid(word)))
        return sentences

    def process(self, msg, reply=True, learn=True):
        '''
        process 'msg'
        add words to db if learn=True
        generate reply if reply=True
        '''
        sentences = self.filter_split_message(msg)
        if len(sentences) < 1:
            return ''
        if learn:
            self.learn(sentences)
        if reply:
            return self.reply(sentences[-1])
        else:
            return ''

    def learn(self, sentences):
        '''
        learn from sentences
        '''
        def learn_sentence(sentence):
            words = sentence.split()

            hashval = hash(sentence)

            if hashval not in self.lines:
                self.lines[hashval] = [sentence, 1]
                for idx, word in enumerate(words):
                    if word in self.words:
                        self.words[word].append((hashval, idx))
                    else:
                        self.words[word] = [(hashval, idx)]
            else:
                self.lines[hashval][1] += 1
        [learn_sentence(sentence) for sentence in sentences]

    def reply(self, sentence):
        '''
        generate reply from a sentence
        '''
        orig_sentence = sentence
        words = sentence.split()
        if len(words) <= 0:
            return ''

        # take a random word as start
        sentence = [random.choice(words)]

        # build the left edge
        done = False
        while not done:
            words_entry = random.choice(self.words[sentence[0]])
            line = self.lines[words_entry[0]][0]
            line_words = line.split()

            word_pos = words_entry[1]

            for i in range(random.randint(self.min_context_depth, self.max_context_depth)):
                if (word_pos - i) < 0:
                    done = True
                    break
                else:
                    word = line_words[word_pos - 1]
                    if word not in sentence:
                        sentence.insert(0, word)
                if (word_pos - i) == 0:
                    done = True
                    break

        # build the right edge
        done = False
        while not done:
            words_entry = random.choice(self.words[sentence[-1]])
            line = self.lines[words_entry[0]][0]
            line_words = line.split()

            word_pos = words_entry[1]

            for i in range(random.randint(self.min_context_depth, self.max_context_depth)):
                if (word_pos + i) >= len(line_words):
                    done = True
                    break
                else:
                    word = line_words[word_pos + i]
                    if word not in sentence:
                        sentence.append(word)

        reply_str = ' '.join(sentence).strip()

        if reply_str == orig_sentence.strip():
            return ''
        else:
            return reply_str
