from typing import List, Union

# Number of children = Number of keys + 1
class Node:
    def __init__(self, isLeaf: bool = False):
        self.keys: List[int] = []
        self.children: List[Node] = []
        self.leaf = isLeaf

class BTree:
    def __init__(self, degree):
        self.root = Node(True)
        self.degree = degree
    
    # The main recursive function for searching
    def _search(self, key: int, node: Node):
        idx = 0

        # Iterating over the keys until we have found the key just smaller than the search key
        while idx < node.keys.__len__() and key > node.keys[idx]:
            idx += 1
        
        # After iterating the counter again, checking if we are in the range of keys and if the next one is the search key
        if idx < node.keys.__len__() and key == node.keys[idx]:
            return (node, idx)
        
        # If it is a leaf node, it has no children, which means we can't search further and search key isn't found
        elif node.isLeaf:
            return None

        # Current key is not the search key, but since children exist, search in them
        else:
            return self._search(key, node.children[idx])
        

    # The public exposed method to be called for searching
    def search(self, key: int):
        return self._search(key, self.root)

    