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

    def known(self, word):
        '''
        Check, if `word` is present in the store

        :param word: target word
        :type word: str

        :return: presence of `word` in the store
        :rtype: bool
        '''
        return False

    def next_words(self, word):
        '''
        Return all words related to `word`

        :param word: target word
        :type word: str

        :return: words related to `word`
        :rtype list[tuple(word, score)]
        '''
        return [('', 0)]
