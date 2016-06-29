import redis


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
        '''
        Insert data into the store
        `next_word` was seen after `word`

        :param word: target word
        :param next_word: word seen after `word`

        :type word: str
        :type next_word: str
        '''
        key = self._key(word)
        if not self.db.exists(key):
            self.db.hmset(key, {next_word: 1})
        else:
            self.db.hincrby(key, next_word)

    def relation_count(self, word):
        '''
        Return number of relations for `word`

        :param word: target word
        :type word: str

        :return: number of relations for `word`
        :rtype: int
        '''
        key = self._key(word)
        if self.db.exists(key):
            return self.db.hlen(key)
        else:
            return 0

    def known(self, word):
        '''
        Check if `word` is present in the store

        :param word: target word
        :type word: str

        :return: presence of `word` in the store
        :rtype: bool
        '''
        return self.db.exists(self._key(word))

    def next_words(self, word):
        '''
        Return all next words for `word`

        :param word: target word
        :type word: str

        :return: words seen after `word`
        :rtype: list[tuple(word, score)]
        '''
        return self.db.hgetall(self._key(word)).items()
