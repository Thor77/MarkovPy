import pytest
from markov.markov import is_smiley, prepare_line, re_url


@pytest.mark.parametrize('possible_smiley,expected', [
    (':)', True),
    (':(', True),
    (':D', True),
    ('(:', True),
    ('):', True),
    ('D:', True),
    ('::', False),
    (':t', False),
    (':a', False),
    ('test', False)
])
def test_is_smiley(possible_smiley, expected):
    assert is_smiley(possible_smiley) == expected


@pytest.mark.parametrize('possible_url,expected', [
    ('http://example.com', True),
    ('https://example.com', True),
    ('htp://example.com', False),
    ('test', False)
])
def test_url(possible_url, expected):
    assert bool(re_url.match(possible_url)) == expected


@pytest.mark.parametrize('line,words', [
    ('hello, how are you?', ['hello,', 'how', 'are', 'you?', '\n']),
    ('hey :D', ['hey', ':D', '\n']),
    ('MY new site: https://EXAMPLE.COM',
        ['my', 'new', 'site:', 'https://EXAMPLE.COM', '\n'])
])
def test_prepare_line(line, words):
    assert prepare_line(line) == words
