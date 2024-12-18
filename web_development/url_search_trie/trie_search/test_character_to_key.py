from trie_search.trie import character_to_key
import pytest


def test_standard_char():
    assert character_to_key("a") == 0
    assert character_to_key("c") == 2
    assert character_to_key("G") == 6
    assert character_to_key("Z") == 25


def test_unique_char():
    assert character_to_key("'") == 26
    assert character_to_key("?") == 26
    assert character_to_key(".") == 26


def test_underline_char():
    assert character_to_key("_") == 26


def test_failure():
    with pytest.raises(TypeError):
        (character_to_key("ABC"))

def integers():
    assert character_to_key("4") == 26

def test_something_crazy():
    assert character_to_key(" ") == 26
