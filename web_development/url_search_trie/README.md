# Search Trie Project

A project for crawling web pages, storing the resulting text in a special data structure known as a **trie** and using it to implement a search interface.

Composed of:
- Part 0: A helper function and some basic tests.
- Part 1: A `Trie` data type for use in search.
- Part 2: A web crawler, designed to populate the Trie.
- Part 3: A search interface using Flask

Explanation of subsequent parts:

## Part 0 - `character_to_key` function and relevant tests

The character_to_key funciton as a relevant helper function with the below specs:
- Keys  treated as if they are made of lower case characters and `_`.
- Characters corresponding to the numeric values 0-26, with 'a' = 0, 'z' = 25, and '_' = 26.
- A-Z treated as 0-25, identical to their lower case form.
- Any other character (such as a number or punctuation) will correspond to 26/'_'.

## Part 1 - Trie and Trie_Node classes

- The Trie is an ABC which requires:
    - `__getitem__`
    - `__setitem__`
    - `__delitem__`
    - `__iter__`
    - `__len__`
-  with an implemented a method `wildcard_search(s: str) -> Iterable[tuple[str, Any]]` that allows fuzzy searching for strings.

## Part 2 - Web Crawler

- Composed of a web crawler that gathers all of the words on a website and make them searchable.
- This also contains helper functions in 'utils.py'.
- A function that builds thd data structure for the Trie using an index function.


## Part 3 - Search Interface

- A Flask search interface with CSS formatting and relevant pages for search indexing and results.
