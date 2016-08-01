from markov.markov import Word


class Store:
    '''
    A generic store for markov-data
    '''

    def insert(self, word, next_word):
        '''
        Create a relation between `word` and `next_word`
        '''
        pass

    def relation_count(self, word):
        '''
        Count relations to `word`

        :param word: target word
        :type word: str

        :return: number of relations to `word`
        :rtype: int
        '''
        return 0

    def next_words(self, word):
        '''
        Return all words related to `word`

        :param word: target word
        :type word: str

        :return: words related to `word`
        :rtype [markov.markov.Word]
        '''
        return [Word('', score=0)]

    def clear(self):
        '''
        Remove all words and relations from the store
        '''

    def __contains__(self, word):
        '''
        Check, if `word` is present in the store

        :param word: target word
        :type word: str

        :return: presence of `word` in the store
        :rtype: bool
        '''
        return False

    def __len__(self):
        '''
        Return count of all known words

        :return: count of all known words
        :rtype: int
        '''
        return 0
