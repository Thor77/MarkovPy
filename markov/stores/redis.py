import redis
from markov.markov import Word


class Redis:
    def __init__(self, host='localhost', port=6379, dbid=0, prefix='markovpy'):
        '''
        Initialize a redis-store for markov-data

        :param host: host for redis-db
        :param port: port for redis-db
        :param dbid: id for redis-db
        :param prefix: prefix for redis-keys

        :type host: str
        :type port: int
        :type dbid: int
        :type prefix: str
        '''
        self.db = redis.StrictRedis(host=host, port=port, db=dbid)
        self.prefix = prefix

    def _key(self, word):
        '''
        prefix ``word`` with db-prefix

        :param word: word to gen key for
        :type word: str
        :return: prefixed ``word``
        :rtype: str
        '''
        return ':'.join((self.prefix, word))

    def insert(self, word, next_word):
        key = self._key(word)
        if not self.db.exists(key):
            self.db.hmset(key, {next_word: 1})
        else:
            self.db.hincrby(key, next_word)

    def relation_count(self, word):
        key = self._key(word)
        if self.db.exists(key):
            return self.db.hlen(key)
        else:
            return 0

    def next_words(self, word):
        return [
            Word(w.decode('utf-8'), int(score))
            for w, score in self.db.hgetall(self._key(word)).items()
        ]

    def clear(self):
        for key in self.db.keys(self._key('*')):
            self.db.delete(key)

    def __contains__(self, word):
        return self.db.exists(self._key(word))

    def __len__(self):
        return len(self.db.keys(self._key('*')))
