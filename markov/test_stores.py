import pytest
from markov.stores import Pickle, Redis


@pytest.mark.parametrize('store', [
    Pickle('test.pickle'),
    Redis(prefix='markovpytest')
])
def test_stores(store):
    store.insert('test', 'test2')
    assert len(store) == 1
    assert store.relation_count('test') == 1
    assert store.known('test')
    assert store.next_words('test') == [('test2', 1)]
    store.insert('test', 'test2')
    assert store.next_words('test') == [('test2', 2)]
    store.insert('test', 'test3')
    assert sorted(store.next_words('test')) ==\
        sorted([('test2', 2), ('test3', 1)])
