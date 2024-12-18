# imports
from .utils import get_links, get_text, fetch_html, ALLOWED_DOMAINS
from .trie import Trie, Trie_Node, character_to_key
from bs4 import BeautifulSoup



def crawl_site(start_url: str, max_depth: int) -> dict[str, list[str]]:
    """
    Given a starting URL, return a mapping of URLs mapped to words that appeared on that page.

    Important: In addition to following max_depth rule, pages must not be visited twice
    from a single call to crawl_site.

    Parameters:

        start_url - URL of page to start crawl on.
        max_depth - Maximum link depth into site to visit.
                    Links from the start page would be depth=1, links from those depth=2, and so on.

    Returns:
        Dictionary mapping strings to lists of strings.

        Dictionary keys: URLs of pages visited.
        Dictionary values: lists of all words that appeared on a given page.
    """
    
    results = {}

    # create set to track accessed sites
    previously_accessed_urls = set()
    current_depth = 0

    def get_local_data(current_url: str) -> list[str, list[str]]:
        """
        HELPER FUNCTION - process the function imports - GET RID OF
        """
        relevant_html = fetch_html(current_url)
        
        bs_parser = BeautifulSoup(relevant_html, 'html.parser')

        for data in bs_parser(['style', 'script']):
            # remove tags
            data.decompose()

        # this is majority of processing time in web.py
        page_text = bs_parser.get_text(separator=' ', strip=True)    
        local_words = page_text.split()    

        # create a dictionary associating the key of the url with the values of words
        relevant_links = get_links(relevant_html, current_url)
        return relevant_links, local_words
    

    def crawl_local_level(current_url: str, current_depth: int) -> dict[str, list[str]]:

        # if url has been used before exist recursion
        if current_url in previously_accessed_urls or current_depth > max_depth:
            return

        # if url has not been used before add to set to prevent future use
        previously_accessed_urls.add(current_url)

        # get links and the words from the applicable html
        relevant_links, local_words = get_local_data(current_url)

        results[current_url] = local_words

        # Prevention of FetchException raises
        allowed_links = [link for link in relevant_links if \
                         any(link.startswith(domain) for domain in ALLOWED_DOMAINS)]

        # recursive run at each level, looping through the lists of new subsequt urls
        if current_depth < max_depth:
            for subsequent_url in allowed_links:
                crawl_local_level(subsequent_url, current_depth + 1)

    crawl_local_level(start_url, current_depth)
    return results        


def build_index(site_url: str, max_depth: int) -> Trie:
    """
    Given a starting URL, build a `Trie` of all words seen mapped to
    the page(s) they appeared upon.

    Parameters:

        start_url - URL of page to start crawl on.
        max_depth - Maximum link depth into site to visit.

    Returns:
        `Trie` where the keys are words seen on the crawl, and the
        value associated with each key is a set of URLs that word
        appeared on.
    """
    t = Trie()

    def recursive_traversal(node: Trie_Node, word: str, url: str):
        """
        Helper function to traverse and insert words into the Trie.
        For each word, we add the URL to the set of values.
        """
        if not word:
            node.end_of_key = True
            node.value.add(url) 
            return

        char = word[0]
        index = character_to_key(char)

        # confirm node existence
        if index >= len(node.children):
            node.children.extend([None] * (index - len(node.children) + 1))

        # if child node is None, create Trie_Node obj
        if node.children[index] is None:
            node.children[index] = Trie_Node()

        # run recursion on the rest of the word
        recursive_traversal(node.children[index], word[1:], url)

    dict_results = crawl_site(site_url, max_depth)
    # add results to the Trie
    for url, words in dict_results.items():
        for word in words:
            recursive_traversal(t.root, word, url)

    return t



# References
# https://www.geeksforgeeks.org/remove-all-style-scripts-and-html-tags-using-beautifulsoup/ - cleaning text using BeautifulSoup
