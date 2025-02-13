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

    # Method to split a full child
    def _split_child(self, parent: Node, idx: int):
        degree = self.degree

        full_child = parent.children[idx]

        # Create a new node and add it to parent's list of children
        new_child = Node(full_child.leaf)
        parent.children.insert(idx + 1, new_child)

        # Insert the median of the full child full_child into node
        parent.keys.insert(idx, full_child.keys[degree - 1])

        # Split apart full_child's keys into full_child & new_child
        new_child.keys = full_child.keys[degree : (2 * degree) - 1]
        full_child.keys = full_child.keys[0 : degree - 1]

        # if full_child is not a leaf, we reassign full_child's children to full_child & new_child
        if not full_child.leaf:
            new_child.children = full_child.children[degree : 2 * degree]
            full_child.children = full_child.children[0:degree]

    # Insertion into a non-full node
    def _insert_non_full(self, curr: Node, key: int):
        degree = self.degree
        idx = len(curr.keys) - 1

        # If the current node is a leaf, find the correct spot to insert the key
        # Basically a loop to insert in a sorted list of keys, starting from the end
        if curr.leaf:
            curr.keys.append(None)
            while idx >= 0 and key < curr.keys[idx]:
                curr.keys[idx + 1] = curr.keys[idx]
                idx -= 1
            curr.keys[idx + 1] = key

        # If not a leaf, find the correct subtree to insert the key
        else:
            # Find the child which is just greater than the key
            while idx >= 0 and key < curr.keys[idx]:
                idx -= 1
            idx += 1

            # If child node is full, split it
            if len(curr.children[idx].keys) == (2 * degree) - 1:
                self.split_child(curr, idx)
                if key > curr.keys[idx]:
                    idx += 1
            self.insert_non_full(curr.children[idx], key)

    # Main insertion method
    def insert(self, key: int):
        degree = self.degree
        root = self.root

        # If root is full, create a new node - tree's height grows by 1
        if len(root.keys) == (2 * degree) - 1:
            new_root = Node()
            self.root = new_root
            new_root.children.insert(0, root)
            self.split_child(new_root, 0)
            self.insert_non_full(new_root, key)
        else:
            self.insert_non_full(root, key)
