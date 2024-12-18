from typing import Any, Iterable
from collections.abc import MutableMapping


def character_to_key(char: str) -> int:
    """
    Given a character return a number between [0, 26] inclusive.

    Letters a-z should be given their position in the alphabet 0-25, regardless of case:
        a/A -> 0
        z/Z -> 25

    Any other character should return 26.
    """

    char = char.lower()
    try:
        ascii_code = ord(char)
    # introduce a check for strings, rather than characters
    except TypeError:
        raise TypeError(char)

    # convert character a-z values to ints and non-chars to 26
    if 96 <= ascii_code <= 122:
        return ascii_code - 97
    else:
        return 26


def key_to_char(character):
    """ Helper function used to transform key integer values to characters """
    return chr(character + 97)


class Trie_Node():
    """ An object with attributes for each of the nodes within the Trie data structure """
    def __init__(self):
        self.children = [None] * 27
        self.value = set()
        self.end_of_key = False


    def __repr__(self) -> str:
        children_indices = [index for index, child in enumerate(self.children) if child is not None]
        if self.value is not set():
            return f"Trie_Node(children_indices={children_indices}, value={self.value})"

class Trie(MutableMapping):
    """
    Implementation of a trie class where each node in the tree can
    have up to 27 children based on next letter of key.
    (Using rules described in character_to_key.)

    Must implement all required MutableMapping methods,
    as well as wildcard_search.
    """

    def __init__(self):
        self.root = Trie_Node()


    def _traverse_trie(self, node: Trie_Node, key):
        """ Helper function dedicated to transversing to a Trie end node """
        for char in key:
            index = character_to_key(char)

            if node.children[index] is None:
                node.children[index] = Trie_Node()
            node = node.children[index]
        return node

    
    def _key_exists(self, key: str) -> bool:
            """ Helper function to determine if a key exists in the Trie """
            node = self.root
            for char in key:
                index = character_to_key(char)
                
                # check if Trie_Node index is None, meaning the key doesn't exist
                if node.children[index] is None:
                    raise KeyError(key)
                node = node.children[index]
            return True

    def _error_check(self, key):
        """ Helper function to raise errors if key is not a string"""
        if not isinstance(key, str):
            raise KeyError(key)
        

    def __getitem__(self, key: str) -> Any:
        """
        Given a key, return the value associated with it in the trie.

        If the key has not been added to this trie, raise `KeyError(key)`.
        If the key is not a string, raise `ValueError(key)`
        """
        
        # checks for key input
        self._error_check(key)
        self._key_exists(key)

        node = self._traverse_trie(self.root, key)

        # checking key existence
        while node and node.end_of_key:
            return node.value
        raise KeyError(key)


    def __setitem__(self, key: str, value: Any) -> None:
        """
        Given a key and value, store the value associated with key.

        Like a dictionary, will overwrite existing data if key already exists.

        If the key is not a string, raise `ValueError(key)`
        """
        # check for key input
        self._error_check(key)

        node = self._traverse_trie(self.root, key)

        # Set the value at the end node of the key
        node.value = value
        node.end_of_key = True
        

    def __delitem__(self, key: str) -> None:
        """
        Remove data associated with `key` from the trie.

        If the key is not a string, raise `ValueError(key)`
        """
        
        self._error_check(key)

        node = self.root
        # capture path to node
        path = []

        # iterate through Trie, capturing parent and children nodes
        for char in key[:-1]:
            index = character_to_key(char)
            if node.children[index] is None:
                raise KeyError(key)
            path.append((node, index))
            node = node.children[index]

        # confirm existence of last char in key
        last_char_index = character_to_key(key[-1])
        if node.children[last_char_index] is None:
            raise KeyError(key)

        # delete last node, alter attributes
        last_node = node.children[last_char_index]
        last_node.value = None
        last_node.end_of_key = False

    
        def _delete_relevant_node(node, parent_node, index):
            """ Helper function to remove parents with no children"""
            if not node.end_of_key and not node.children:
                del parent_node.children[index]
                return True  
            return False 

        # move from child to root, deleting relevant nodes
        for parent_node, index in reversed(path):
            if _delete_relevant_node(parent_node, parent_node, index):
                pass


    def __len__(self) -> int:
        """
        Return the total number of entries currently in the trie.
        """
        
        def _count_nodes(node):
            """ Helper function to count the Trie_Nodes in the Trie"""

            count = 0
            if node.value:
                count += 1
            # loop to count each brand in the Trie
            for child in node.children:
                if child is not None:
                    count += _count_nodes(child)
            return count

        return _count_nodes(self.root)


    def __iter__(self) -> Iterable[tuple[str, Any]]:
        """
        Return an iterable of (key, value) pairs for every entry in the trie in alphabetical order.
        """

        def _iter_traverse_trie(node, current_letters):
            """ Helper function to iterate through """
            if node.value:
                # tuple of current sequence of chars, and Trie_Node value
                yield current_letters, node.value

            # index child nodes and assigned their characters
            for char_index, child_node in enumerate(node.children):
                if child_node is not None:
                    yield from _iter_traverse_trie(child_node, current_letters + key_to_char(char_index))

        # run traversal from an empty string
        return _iter_traverse_trie(self.root, "")
    

    def wildcard_search(self, key: str) -> Iterable[tuple[str, Any]]:
        """
        Search for keys that match a wildcard pattern where a '*' can represent any character.

        For example:
            - c?t would match 'cat', 'cut', 'cot', etc.
            - ?? would match any two-letter string.

        Returns: Iterable of (key, value) pairs meeting the given condition.
        """
        def _wildcard_traverse_trie(node, current_key, wildcard):
            """
            Helper function to traverse Trie in case of unknown characters.

            Args:
            node = current trie node
            current_key = key at current point in path
            wildcard = remaining wildcard characters
            
            Output:
            a list of matching strings based on potential wildcard values
            """
            # cases of end of word or regular chars
            if (wildcard == "" or current_key == wildcard) and node.value:
                yield current_key, node.value

            # case of wildcard being an empty string
            if not wildcard:
                return

            for char_index, child_node in enumerate(node.children):
                if child_node is not None:

                    # case where function moves to subsequent nodes to match chars, slicing first wildcard char
                    if wildcard[0] == '*':
                        yield from _wildcard_traverse_trie(child_node, current_key + key_to_char(char_index), wildcard[1:])

                    # case of where char matches wildcard, and function moves to subsequent nodes
                    elif key_to_char(char_index) == wildcard[0]:
                        yield from _wildcard_traverse_trie(child_node, current_key + key_to_char(char_index), wildcard[1:])
        
        matched_wildcards = list(_wildcard_traverse_trie(self.root, "", key))
        return matched_wildcards


# References:
# https://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python - for logic behind classes
# https://www.aleksandrhovhannisyan.com/blog/python-trie-data-structure/ - for iter and wildcard

