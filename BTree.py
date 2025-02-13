from typing import List, Union, Tuple


# Number of children = Number of keys + 1
class Node:
    def __init__(self, isLeaf: bool = False):
        self.keys: List[int] = []
        self.children: List[Node] = []
        self.leaf = isLeaf


class BTree:

    def __init__(self, degree) -> None:
        """
        Inserts a key into the B-Tree, maintaining the B-Tree properties.
        If the root node is full, the tree's height increases by one and the root is split before insertion.
        Args:
            key (int): The key to be inserted into the B-Tree.
        Returns:
            None
        """
        self.root = Node(True)
        self.degree = degree

    @staticmethod
    def is_node_full(node: Node, degree: int) -> bool:
        """
        Checks if a node is full based on the B-Tree properties.
        A node is considered full if it has (2 * degree) - 1 keys.
        Args:
            node (Node): The node to check.
            degree (int): The degree of the B-Tree.
        Returns:
            bool: True if the node is full, False otherwise.
        """
        return len(node.keys) == (2 * degree) - 1

    # The main recursive function for searching
    def __search(self, key: int, node: Node) -> Union[Tuple[Node, int], None]:
        """
        Searches for a key in the B-Tree starting from the given node.
        Args:
            key (int): The key to search for in the B-Tree.
            node (Node): The current node to start the search from.
        Returns:
            Tuple[Node, int]: A tuple containing the node and the index of the key if found.
            None: If the key is not found in the B-Tree.
        """
        idx = 0

        # Iterating over the keys until we have found the key just smaller than the search key
        while idx < len(node.keys) and key > node.keys[idx]:
            idx += 1

        # After iterating the counter again, checking if we are in the range of keys and if the next one is the search key
        if idx < len(node.keys) and key == node.keys[idx]:
            return (node, idx)

        # If it is a leaf node, it has no children, which means we can't search further and search key isn't found
        elif node.leaf:
            return None

        # Current key is not the search key, but since children exist, search in them
        else:
            return self.__search(key, node.children[idx])

    # The public exposed method to be called for searching
    def search(self, key: int) -> Union[Tuple[Node, int], None]:
        """
        Searches for a key in the B-Tree.
        Args:
            key (int): The key to search for in the B-Tree.
        Returns:
            Tuple[Node, int]: A tuple containing the node and the index of the key if found.
            None: If the key is not found in the B-Tree.
        """
        return self.__search(key, self.root)

    # Method to split a full child
    def __split_child(self, parent: Node, idx: int):
        degree = self.degree

        full_child = parent.children[idx]

        # Create a new node and add it to parent's list of children
        new_child = Node(full_child.leaf)
        parent.children.insert(idx + 1, new_child)

        # Insert the median of the full child into parent
        parent.keys.insert(idx, full_child.keys[degree - 1])

        # Split apart full_child's keys into full_child & new_child
        new_child.keys = full_child.keys[degree : (2 * degree) - 1]
        full_child.keys = full_child.keys[0 : degree - 1]

        # if full_child is not a leaf, we reassign full_child's children to full_child & new_child
        if not full_child.leaf:
            new_child.children = full_child.children[degree : 2 * degree]
            full_child.children = full_child.children[0:degree]

    # Insertion into a non-full node
    def __insert_non_full(self, curr: Node, key: int):
        degree = self.degree
        idx = 0

        # Get to the index where the key should be inserted
        while idx < len(curr.keys) and key > curr.keys[idx]:
            idx += 1

        # Now if we are at a leaf node, we can insert the key directly
        if curr.leaf:
            curr.keys.insert(idx, key)

        # If not a leaf, find the correct subtree to insert the key
        else:
            # If child node is full, split it
            if self.is_node_full(curr.children[idx], degree):
                self.__split_child(curr, idx)
                if key > curr.keys[idx]:
                    idx += 1
            self.__insert_non_full(curr.children[idx], key)

    # Main insertion method
    def insert(self, key: int):
        degree = self.degree

        # If root is full, create a new node - tree's height grows by 1
        if self.is_node_full(self.root, degree):
            new_root = Node(False)
            old_root = self.root
            new_root.children.append(old_root)
            self.root = new_root
            self.__split_child(new_root, 0)

        self.__insert_non_full(self.root, key)
