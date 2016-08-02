import pytest
from markov import MarkovPy
from markov.stores import Redis


@pytest.fixture
def clean_store(request):
    store = Redis(prefix='markovpytest')

    def clean():
        store.clear()
    request.addfinalizer(clean)
    return store


@pytest.fixture
def markov(clean_store):
    return MarkovPy(store=clean_store)


def test_learn(markov):
    markov.learn('a b')
    assert 'a' in markov.store
    assert markov.store.next_words('a') == [('b', 1)]


def test_reply(markov):
    markov.learn('c d')
    assert markov.reply('c', min_length=1, max_length=2) in ['c', 'c d']


def test_reply_empty(markov):
    assert markov.reply('e') is None


def test_reply_multi(markov):
    markov.learn('f g')
    markov.learn('f f')
    assert markov.reply('f', min_length=1, max_length=2) in ['f', 'f g', 'f f']


def test_reply_min_length(markov):
    markov.learn('f g')
    assert markov.reply('f', min_length=42) is None


def test_best_known_word(markov):
    markov.learn('f')
    assert markov._best_known_word(['f']) == 'f'
    markov.learn('f g')
    assert markov._best_known_word(['f', 'g']) in ['f', 'g']
    markov.learn('f h')
    assert markov._best_known_word(['f', 'g', 'h']) == 'f'
