import random
import re

import redis

re_smiley = re.compile(r'[8;:=%][-oc*^]?[)(D\/\\]')
re_smiley_reversed = re.compile(r'[)(D\/\\][-oc*^]?[8;:=%]')
re_smiley_asian = re.compile(r'\^[o_.]?\^')
re_smileys = [re_smiley, re_smiley_reversed, re_smiley_asian]
re_url = re.compile(r'(?:(?:https?|ftp):\/\/.*)')
sentence_endings = ['?', '!', '.']

class PyAI:

    def __init__(self, db_prefix='pyai', db_host='localhost', db_port=6379, db_id=0):
        '''
        :param str db_prefix: prefix for redis-keys
        :param str db_host: host for redis-db
        :param int db_port: port for redis-db
        :param int db_id: id for redis-db
        '''
        self.db = redis.StrictRedis(host=db_host, port=db_port, db=db_id)
        self.prefix = db_prefix

    def _words_key(self, word):
        '''
        prefix ``word`` with db-prefix

        :param str word: word to gen key for
        '''
        return ':'.join((self.prefix, word))

    def _is_smiley(self, word):
        '''
        check if ``word`` is a smiley

        :param str word: word to check
        '''
        for re_smiley in re_smileys:
            if re_smiley.match(word):
                return True
        return False

    def prepare_line(self, line):
        '''
        split words to line, lower words, add newlines and remove invalid chars

        :param str line: line to prepare
        '''
        # split line to words and remove words < 3 chars (doesn't remove smileys)
        words_ = line.split()
        words = []
        for word_ in words_:
            word = None
            # prevent smileys and urls from getting lower'd
            if self._is_smiley(word_) or word_ == '<3' or re_url.match(word_):
                word = word_
            else:
                word = word_.lower()
                # filter all non-chars & non-digits from word
                word = ''.join(c for c in word if (c.isalpha() or c.isdigit()) and c != '\n')
            # maybe the word is completely lost now
            if word:
                words.append(word)
                # check if word ended with sentence ending to add \n
                for sentence_ending in sentence_endings:
                    if word_.endswith(sentence_ending):
                        words.append('\n')
                        break
        return words

    def learn(self, line, prepared=False):
        '''
        add line to database

        :param str line: line to add
        :param bool prepared: line was already split to words
        '''
        if prepared:
            words = line
        else:
            words = self.prepare_line(line)
        for i in range(0, len(words)):
            curr_word = words[i]
            if len(words) <= i + 1:
                break
            next_word = words[i + 1]
            word_db_key = self._words_key(curr_word)
            if not self.db.exists(word_db_key):
                self.db.hmset(word_db_key, {next_word: 1})
            else:
                self.db.hincrby(word_db_key, next_word)

    def reply(self, start, min_length=5, max_length=10, prepared=False):
        '''
        generated a reply to ``start``

        :param int min_length: minimal length of reply
        :param int max_length: max length of reply
        :param bool prepared: line was already split to words
        '''
        if prepared:
            start_words = start
        else:
            start_words = self.prepare_line(start)
        # choose best known word to start with
        word_relations = [(word, self.db.hlen(self._words_key(word))) for word in start_words if self.db.exists(self._words_key(word))]
        if not word_relations:
            return None
        if len(word_relations) == 1:
            best_known_word = word_relations[0][0]
        else:
            sorted_word_relations = sorted(word_relations, key=lambda x: x[1])
            highest_num = sorted_word_relations[0][1]
            best_known_words = [sorted_word_relations[0][0]]
            for word, num in word_relations:
                if num == highest_num:
                    best_known_words.append(word)
                else:
                    break
            best_known_word = random.choice(best_known_words)
        # gen answer
        length = random.randint(min_length, max_length)
        answer = [best_known_word]
        while len(answer) < length:
            # get all possible next words
            word_key = self._words_key(answer[-1])
            # key doesn't exist => no possible next words
            if not self.db.exists(word_key):
                break
            possible_words = self.db.hgetall(word_key).items()
            if len(possible_words) == 1:
                word = list(possible_words)[0][0].decode('utf-8')
            else:
                # sort random word but weight
                best_words = [word.decode('utf-8') for word, num in possible_words for i in range(int(num))]
                word = random.choice(best_words)
            # choosen word == line-end => break
            if word == '\n':
                break
            # add to answer
            answer.append(word)
        return ' '.join(answer)

    def process(self, line, learn=True, reply=True):
        '''
        process ``line``

        :param str line: line to process
        :param bool learn: learn from line
        :param bool reply: reply to line (and return answer)
        '''
        prepared_line = self.prepare_line(line)
        if learn:
            self.learn(prepared_line, prepared=True)
        if reply:
            return self.reply(prepared_line, prepared=True)
